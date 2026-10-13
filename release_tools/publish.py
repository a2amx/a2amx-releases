"""Verify a tagged release-only tree, then create one preview Release.

This setup tool is independent of the application wheel. Dry-run is local and
is the default. Publication runs only in the tag-push job; it never pushes Git,
edits the index, deletes an object, moves a tag, or replaces a Release asset.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from types import MappingProxyType
import urllib.error
import urllib.parse
import urllib.request

MAX_ASSET = 32 * 1024 * 1024
MAX_JSON = 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
TAG = re.compile(r"(?:(?P<distribution>[a-z][a-z0-9_]*)-)?v(?P<version>[0-9]+\.[0-9]+\.[0-9]+(?:[a-zA-Z0-9.+-]*))\Z")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,199}\Z")
DIGEST = re.compile(r"[a-f0-9]{64}\Z")
REUSED_SNAPSHOT = "14f6ebccdc9ce94dbbf2cf5ff9f902617f8edbb7"
REUSED_MANIFEST = "a5e9e3229bca8c6b1ce02a7bd21d559e26a587d98f37f13169ac6cd22846489f"
REUSED_WHEEL = "3060c172a9d40ac555ee7773813c9d2220856753072628166e8a648316b1f2de"
PAGES = {"README.md", "docs/INSTALL.md", "docs/FIRST_EXCHANGE.md",
         "docs/UPDATE_AND_UNINSTALL.md", "docs/SUPPORT.md"}


class Refused(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, limit):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise Refused("symlink_in_release_tree")
    try:
        with path.open("rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise Refused("release_file_bound")
            data = stream.read(limit + 1)
    except OSError:
        raise Refused("release_file_unreadable") from None
    if len(data) != info.st_size or len(data) > limit:
        raise Refused("release_file_changed")
    return data


def pairs(items):
    result = {}
    for k, v in items:
        if k in result:
            raise Refused("duplicate_json_key")
        result[k] = v
    return result


def parse(data):
    if len(data) > MAX_JSON:
        raise Refused("json_bound")
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Refused("nonfinite_json")))
    except (ValueError, UnicodeError, RecursionError):
        raise Refused("invalid_release_json") from None


def shape(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise Refused("release_record_shape")


@dataclass(frozen=True)
class Verified:
    tag: str
    files: MappingProxyType
    checksums: MappingProxyType
    notes: str


def verify(root, tag):
    match = TAG.fullmatch(tag) if isinstance(tag, str) else None
    if match is None or match['distribution'] == 'quovisto':
        raise Refused("invalid_tag")
    distribution = match['distribution'] or 'quovisto'
    version = match['version']
    root = Path(root).absolute()
    assets = root / "assets" / tag
    sums = read(assets / "SHA256SUMS", MAX_JSON)
    try:
        lines = sums.decode("ascii").splitlines()
    except UnicodeError:
        raise Refused("invalid_checksums") from None
    hashes = {}
    for line in lines:
        match = re.fullmatch(r"([a-f0-9]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]{0,199})", line)
        if not match or match[2] == "SHA256SUMS" or match[2] in hashes:
            raise Refused("invalid_checksums")
        hashes[match[2]] = match[1]
    if not 6 <= len(hashes) <= 10:
        raise Refused("asset_count")
    if {p.name for p in assets.iterdir()} != set(hashes) | {"SHA256SUMS"}:
        raise Refused("asset_inventory_mismatch")
    blobs = {name: read(assets / name, MAX_ASSET) for name in hashes}
    if sum(map(len, blobs.values())) > MAX_TOTAL or any(sha(blobs[n]) != h for n, h in hashes.items()):
        raise Refused("asset_digest_or_bound")
    if "RELEASE.json" not in blobs:
        raise Refused("release_record_missing")
    release = parse(blobs["RELEASE.json"])
    fields = {"schema", "tag", "version", "status", "qualification", "omission_reason", "wheel", "pages"}
    if distribution != 'quovisto':
        fields |= {'source_commit', 'snapshot_commit'}
    shape(release, fields)
    if (type(release["schema"]) is not int or release["schema"] != 1 or release["tag"] != tag
            or release["version"] != version or release["status"] != "preview"):
        raise Refused("release_identity")
    wheel = release["wheel"]
    if not isinstance(wheel, str) or not NAME.fullmatch(wheel) or wheel != distribution + "-" + version + "-py3-none-any.whl":
        raise Refused("wheel_identity")
    expected = {wheel, "RELEASE.json", "RELEASE_NOTES.md", "SNAPSHOT_MANIFEST.json", "S1_BUILD.json", "WHEEL_SHA256SUMS"}
    if release["qualification"] == "included" and release["omission_reason"] is None:
        expected.add("QUALIFICATION.json")
    elif release["qualification"] != "omitted" or release["omission_reason"] != "qualification_deferred":
        raise Refused("qualification_mode")
    if set(blobs) != expected:
        raise Refused("unexpected_release_asset")
    build = parse(blobs["S1_BUILD.json"])
    if not isinstance(build, dict) or not isinstance(build.get("wheel"), dict):
        raise Refused("build_binding")
    if (type(build.get("schema")) is not int or build["schema"] != 1 or build.get("tag") != tag
            or build.get("snapshot_manifest_sha256") != hashes["SNAPSHOT_MANIFEST.json"]
            or build.get("wheel", {}).get("filename") != wheel
            or build["wheel"].get("size") != len(blobs[wheel])
            or build["wheel"].get("sha256") != hashes[wheel]
            or build["wheel"].get("distribution") != distribution
            or build["wheel"].get("version") != version):
        raise Refused("build_binding")
    if blobs["WHEEL_SHA256SUMS"] != (hashes[wheel] + "  " + wheel + "\n").encode():
        raise Refused("wheel_only_checksums")
    if distribution != 'quovisto':
        snapshot = parse(blobs['SNAPSHOT_MANIFEST.json'])
        if (distribution != 'a2amx' or version != '0.0.0' or release['qualification'] != 'included'
                or not isinstance(release['source_commit'], str)
                or not re.fullmatch('[a-f0-9]{40}', release['source_commit'])
                or release['snapshot_commit'] != REUSED_SNAPSHOT
                or build.get('snapshot_commit') != release['snapshot_commit']
                or hashes['SNAPSHOT_MANIFEST.json'] != REUSED_MANIFEST
                or not isinstance(snapshot, dict) or snapshot.get('tag') != 'v0.0.0'
                or any(build.get(key) != snapshot.get(key) for key in ('commit', 'tree', 'internal_version'))):
            raise Refused('reused_snapshot_binding')
    if "QUALIFICATION.json" in blobs:
        q = parse(blobs["QUALIFICATION.json"])
        if not isinstance(q, dict) or not isinstance(q.get("qualification"), dict):
            raise Refused("qualification_binding")
        binding = {"wheel_sha256": hashes[wheel], "build_record_sha256": hashes["S1_BUILD.json"],
                   "kit_source_sha256": build.get("snapshot_tree_sha256")}
        distribution_only = q.get('schema') == 'quovisto.distribution-qualification.v1'
        if distribution != 'quovisto' and not distribution_only:
            raise Refused('distribution_qualification_required')
        if distribution_only:
            differences = ['product_profile.json:distribution', 'METADATA:Name', 'RECORD', 'dist-info directory']
            change = build.get('distribution_change') or {}
            if (distribution != 'a2amx' or version != '0.0.0' or build.get('source_tag') != 'v0.0.0'
                    or q['qualification'].get('kind') != 'distribution_only'
                    or q['qualification'].get('installed_runtime') != 'not_run'
                    or q['qualification'].get('comparison_scope') != 'member_contents'
                    or q['qualification'].get('snapshot_commit') != release.get('snapshot_commit')
                    or q['qualification'].get('permitted_differences') != differences
                    or q['qualification'].get('all_other_member_bytes_equal') is not True
                    or change.get('permitted_differences') != differences
                    or change.get('all_other_member_bytes_equal') is not True
                    or change.get('comparison_scope') != 'member_contents'
                    or change.get('original_distribution') != 'quovisto'
                    or change.get('original_wheel_sha256') != REUSED_WHEEL):
                raise Refused('distribution_qualification_binding')
        if ((q.get("schema") != "quovisto.release-qualification.v1" and not distribution_only) or q.get("binding") != binding
                or q.get("qualification", {}).get("release_status") != "preview"
                or q["qualification"].get("release_word_inferred") is not False):
            raise Refused("qualification_binding")
    try:
        notes = blobs["RELEASE_NOTES.md"].decode("utf-8")
    except UnicodeError:
        raise Refused("release_notes_encoding") from None
    if not notes.strip() or re.search(r"\{\{[A-Z_][A-Z0-9_]*\}\}", notes):
        raise Refused("release_notes_unfilled")
    if release["qualification"] == "omitted" and "Qualification record omitted" not in notes:
        raise Refused("qualification_omission_not_disclosed")
    pages = release["pages"]
    if not isinstance(pages, dict) or set(pages) != PAGES:
        raise Refused("page_inventory")
    for name, digest in pages.items():
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise Refused("page_digest")
        data = read(root / name, MAX_JSON)
        if sha(data) != digest or re.search(rb"\{\{[A-Z_][A-Z0-9_]*\}\}", data):
            raise Refused("page_changed_or_unfilled")
    blobs["SHA256SUMS"] = sums
    hashes["SHA256SUMS"] = sha(sums)
    return Verified(tag, MappingProxyType(blobs), MappingProxyType(hashes), notes)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise Refused("api_redirect_refused")


class API:
    def __init__(self, repository, token):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or not token:
            raise Refused("publication_identity")
        self.repository, self.token = repository, token
        self.opener = urllib.request.build_opener(NoRedirect)

    def request(self, method, suffix, body=None, *, asset=None, missing=False):
        host = "uploads.github.com" if asset else "api.github.com"
        data = asset[1] if asset else (json.dumps(body).encode() if body is not None else None)
        headers = {"Authorization": "Bearer " + self.token, "Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2026-03-10"}
        if data is not None:
            headers["Content-Type"] = "application/octet-stream" if asset else "application/json"
        req = urllib.request.Request("https://" + host + "/repos/" + self.repository + suffix,
                                     data=data, headers=headers, method=method)
        try:
            with self.opener.open(req, timeout=60) as response:
                raw = response.read(MAX_JSON + 1)
        except urllib.error.HTTPError as exc:
            if missing and exc.code == 404:
                return None
            raise Refused("api_http_" + str(exc.code)) from None
        except (OSError, urllib.error.URLError):
            raise Refused("api_outcome_unconfirmed") from None
        return parse(raw)


def refuse_existing_release(api, tag):
    """The authenticated list includes drafts; tag lookup alone does not.

    Exhaust the bounded inventory before any POST. A retained draft belongs to
    the owner's recovery decision, never to a retry of this workflow.
    """
    seen = set()
    for page in range(1, 101):
        rows = api.request("GET", f"/releases?per_page=30&page={page}")
        if not isinstance(rows, list) or len(rows) > 30:
            raise Refused("release_inventory_unconfirmed")
        for row in rows:
            if (not isinstance(row, dict) or type(row.get("id")) is not int or row["id"] <= 0
                    or not isinstance(row.get("tag_name"), str) or not row["tag_name"]
                    or row["id"] in seen):
                raise Refused("release_inventory_unconfirmed")
            seen.add(row["id"])
            if row["tag_name"] == tag:
                raise Refused("release_already_exists")
        if len(rows) < 30:
            return
    raise Refused("release_inventory_bound")


def publish(verified, api, commit):
    """Each object is created once; any ambiguity stops, retaining the draft."""
    tag = verified.tag
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise Refused("event_commit_required")
    ref = api.request("GET", "/git/ref/tags/" + urllib.parse.quote(tag, safe=""))
    target = ref.get("object") if isinstance(ref, dict) else None
    if not isinstance(target, dict) or target.get("type") != "commit" or target.get("sha") != commit:
        raise Refused("tag_commit_mismatch")
    refuse_existing_release(api, tag)
    if api.request("GET", "/releases/tags/" + urllib.parse.quote(tag, safe=""), missing=True) is not None:
        raise Refused("release_already_exists")
    release = api.request("POST", "/releases", {"tag_name": tag, "target_commitish": commit,
        "name": tag, "body": verified.notes, "draft": True, "prerelease": True,
        "generate_release_notes": False, "make_latest": "false"})
    identity = release.get("id") if isinstance(release, dict) else None
    if type(identity) is not int or identity <= 0 or release.get("draft") is not True or release.get("tag_name") != tag or release.get("assets") != []:
        raise Refused("release_creation_unconfirmed")
    for name, data in sorted(verified.files.items()):
        asset = api.request("POST", f"/releases/{identity}/assets?name=" + urllib.parse.quote(name, safe=""), asset=(name, data))
        if (not isinstance(asset, dict) or asset.get("name") != name or asset.get("size") != len(data)
                or asset.get("digest") != "sha256:" + verified.checksums[name] or asset.get("state") != "uploaded"):
            raise Refused("asset_upload_unconfirmed")
    assets = api.request("GET", f"/releases/{identity}/assets?per_page=100")
    if not isinstance(assets, list) or len(assets) != len(verified.files):
        raise Refused("uploaded_inventory_unconfirmed")
    found = {a.get("name"): a for a in assets if isinstance(a, dict)}
    if set(found) != set(verified.files) or any(found[n].get("size") != len(verified.files[n])
            or found[n].get("digest") != "sha256:" + verified.checksums[n]
            or found[n].get("state") != "uploaded" for n in verified.files):
        raise Refused("uploaded_inventory_unconfirmed")
    result = api.request("PATCH", f"/releases/{identity}", {"draft": False, "prerelease": True, "make_latest": "false"})
    if not isinstance(result, dict) or result.get("id") != identity or result.get("draft") is not False or result.get("prerelease") is not True or result.get("tag_name") != tag:
        raise Refused("release_publication_unconfirmed")
    return {"state": "published", "tag": tag, "release_id": identity,
            "status": "preview", "assets": dict(verified.checksums)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--tag", default=os.environ.get("RELEASE_TAG"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    try:
        verified = verify(Path(args.root).resolve(), args.tag)
        if not args.execute:
            print(json.dumps({"state": "verified_dry_run", "tag": verified.tag,
                              "assets": dict(verified.checksums)}, sort_keys=True))
            return 0
        if (os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_EVENT_NAME") != "push"
                or os.environ.get("GITHUB_REF") != "refs/tags/" + verified.tag):
            raise Refused("tag_push_job_required")
        commit = os.environ.get("GITHUB_SHA", "")
        if not re.fullmatch(r"[a-f0-9]{40}", commit):
            raise Refused("event_commit_required")
        head = subprocess.run(["git", "-C", args.root, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=10, check=True).stdout.strip()
        if head != commit:
            raise Refused("checkout_event_mismatch")
        result = publish(verified, API(os.environ.get("GITHUB_REPOSITORY", ""), os.environ.get("GITHUB_TOKEN", "")), commit)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (Refused, OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as exc:
        reason = str(exc) if isinstance(exc, Refused) else "publication_not_confirmed"
        print(json.dumps({"state": "not_confirmed", "reason": reason}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
