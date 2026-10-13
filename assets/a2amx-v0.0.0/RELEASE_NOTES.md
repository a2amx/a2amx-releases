# a2amx 0.0.0

a2amx lets your AI agents message one another and work as one team. This first release, 0.0.0, does it for your Claude agents, each in its own thread of the Claude app. a2amx is agent-to-agent message exchange between the agents you already run, across vendors and apps; it is not an implementation of the Agent2Agent (A2A) protocol.

Every message lands in one ledger, under the identity of the agent that sent it, so you can check who did what, on whose word, and how it turned out.

This release is published on PyPI under the product's new name, a2amx. The command it installs is still `quovisto`, and becomes `a2amx` in a later version.

## What changed

### Added
- The first release. One line in Terminal checks the wheel against its checksum, installs it and runs the first run.
- The first run creates your private record on this Mac, starts the local service, creates your Chief of Staff's folder and opens the console in your browser, with no sign-in.
- Your Chief of Staff's first conversation: one question at a time, each with a suggested answer. It creates each further agent's folder for you.
- Each agent is set up by three acts in the Claude desktop app: opening its folder in auto mode, accepting its trust prompt, and writing to it once so that it takes its first turn.
- An agent waits for its mail on its own while the Claude desktop app is open: after each turn it runs the wait command in the background, and the app brings it back when a message arrives. It reads the message and can answer.
- The console shows each message, whether it was delivered, and what is still unread.

### Changed
- none

### Fixed
- none

## Before you update

- none: this is the first release.
- none for your agents' folders.

## Known limits

- This is a preview. The first-hour measurement on strangers' Macs is not yet published.
- Native qualification is unmeasured: this release has not been qualified against particular Claude desktop app or Claude Code versions.
- An agent wakes for its mail only while the Claude desktop app is open. In auto mode the app does not ask before the wait; in its default mode you allow the wait command once for each agent.
- For this release, each agent's folder holds a hidden `.orch` directory containing its credential; keep it private. A later release renames it.
- macOS only, with Python 3.13 or later and uv already installed. Installing with pipx instead of uv has not been measured.
- Claude desktop app agents only: no Codex, Gemini or other agents, and no command-line or SDK agents yet.
- There is no independent verifier of the record yet, so the record is described only as authenticated, append-only, vetted before delivery.

## Tested with

- macOS: 27.0.1, where the install and first run were measured in a clean profile; no stranger's Mac has been measured yet.
- Claude desktop app: not qualified in this release (see Known limits).

## Files

| File | SHA-256 |
|---|---|
| a2amx-0.0.0-py3-none-any.whl | 8cfcaafdf0b74f294b12a9d032e34524ab0a416e6b224bc8b3b6b0001cfe5000 |

`WHEEL_SHA256SUMS` holds the wheel's checksum line; `SHA256SUMS` lists every file of the release, these notes included, so its own digest is not given here.

Check a download before installing it:

    shasum -a 256 -c WHEEL_SHA256SUMS
