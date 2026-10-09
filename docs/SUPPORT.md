# Support

If something did not happen as the [install](INSTALL.md) or [first exchange](FIRST_EXCHANGE.md) page describes, tell us by opening an issue at https://github.com/psqr-ai/quovisto-releases/issues. Issues are public: anyone can read what you write there.

## What to send

1. **The version you installed:**
   ```sh
   quovisto --version
   ```
   Send the line it prints.
2. **The check's output:**
   ```sh
   quovisto doctor
   ```
3. **Your macOS version and your Claude desktop app version.** In the app, the version is under **Claude > About Claude** in the menu bar.
4. **What you did, what you expected, and what happened instead,** in a few sentences. Say which step of which page you were on.

## What never to send

- **No transcript** of an agent's session, and no message from your record. They can hold your code and your words.
- **No token, password or key**, and no file from `~/.quovisto`. If an output you are about to send shows a long random string, remove it first.
- **No screenshot of a terminal or console that shows a credential.**

We never ask for any of these. If someone does, it is not us.

## Before you write

- `quovisto doctor` names a missing prerequisite in one sentence. Install what it names, and run the step again.
- If an agent has not answered a message, check that the Claude desktop app is open: an agent waits for its mail only while the app is open. If the app asked you to allow the wait command and you did not, write to that agent once; it reads its mail and asks again.
- If the console asks for its credential (for example after you cleared your browser's data), run `quovisto setup` again: it opens the console the same way. Or choose the file `~/.quovisto/run/.ui_token` when the console asks; in the file chooser, Command-Shift-. shows hidden files.
- If you have set `ANTHROPIC_API_KEY` in your shell, a Claude Code session started from that shell bills that key instead of your Claude subscription. Agents opened in the Claude desktop app do not see it. `quovisto doctor` names such a variable without showing its value.
