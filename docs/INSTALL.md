# Install Quovisto

You install once, with one line in Terminal. After that, each agent takes you three small acts in the Claude desktop app: opening its folder in auto mode, trusting it, and writing to it once. From then on it waits for its mail on its own while the app is open. That is all the setup there is. Nothing on these pages asks you to set an environment variable, and nothing needs one.

## Before you start

You need these on your Mac:

- **macOS.** The release notes name the macOS versions each release was tested on.
- **Python 3.13** or later.
- **uv**, the Python tool installer. `pipx` works too; this page shows uv.
- **The Claude desktop app**, signed in to your Claude account.

Install any that are missing before step 1. If one is still missing, the install line stops: without uv, Terminal says `uv: command not found`; for the others, the first run names what is missing in one sentence.

## 1. Install and first run

Paste this one line into Terminal and press Return:

```sh
d="$(mktemp -d)" && cd "$d" && curl -fsSLO https://github.com/psqr-ai/quovisto-releases/releases/download/v0.0.0/quovisto-0.0.0-py3-none-any.whl && curl -fsSLO https://github.com/psqr-ai/quovisto-releases/releases/download/v0.0.0/WHEEL_SHA256SUMS && shasum -a 256 -c WHEEL_SHA256SUMS && uv tool install -q --force ./quovisto-0.0.0-py3-none-any.whl && "$(uv tool dir --bin)/quovisto" setup
```

It downloads the wheel, `quovisto-0.0.0-py3-none-any.whl`, and its checksum file, `WHEEL_SHA256SUMS`, into a new temporary folder, checks the wheel against it before anything is installed, installs it, and then runs the first run, `quovisto setup`. If the check fails, nothing is installed; tell us (see [Support](SUPPORT.md)).

The first run:
- creates your private record on this Mac;
- starts the local service;
- creates your Chief of Staff's folder;
- opens the console in your browser, and prints its link in case the browser does not open.

The console listens on this Mac only, and you do not sign in to it. From any new Terminal window, the `quovisto` command is then ready to use; there is nothing else to set up.

**If you would rather check the file by hand first:** download `quovisto-0.0.0-py3-none-any.whl` and `WHEEL_SHA256SUMS` from the [release page](https://github.com/psqr-ai/quovisto-releases/releases) into one folder, and in that folder run:

```sh
shasum -a 256 quovisto-0.0.0-py3-none-any.whl
```

The printed value must equal the value in `WHEEL_SHA256SUMS`. If it does not, do not install it, and tell us. If it does, install that same file from that folder, with its first run:

```sh
uv tool install -q --force ./quovisto-0.0.0-py3-none-any.whl && "$(uv tool dir --bin)/quovisto" setup
```

## 2. Open your Chief of Staff

In the Claude desktop app, start a Claude Code session in the folder the first run printed, `~/agents/Chief`, choose auto mode when the app asks how to run it, and accept the app's prompt to trust that folder. Then write to it once, anything, for example "Hello", so that it takes its first turn. From then on it waits for its mail on its own while the app is open.

Your Chief of Staff takes it from there. Continue with [your first exchange](FIRST_EXCHANGE.md).

## If something looks wrong

```sh
quovisto doctor
```

It reports what is running, and names any missing prerequisite in one sentence. This check is optional; it is not a setup step.

## What you did

1. **Install:** the one line in step 1, once. It includes the first run.
2. **Your Chief of Staff:** you opened its folder in auto mode, trusted it, and wrote to it once.
3. **Each further agent:** you will open its folder in auto mode, trust it, and write to it once.
