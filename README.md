# Quovisto

Quovisto keeps one record of what your coding agents say to each other and do. You run the agents; Quovisto carries their messages between them and keeps the record.

Every message in that record is **authenticated, append-only, vetted before delivery**:
- **Authenticated:** each agent sends with its own credential, and each message records which agent's credential sent it.
- **Append-only:** Quovisto adds each new entry at the end of the record and never edits an earlier one.
- **Vetted before delivery:** each message is checked before it reaches the agent it is addressed to.

**This is a preview, and it stays a preview until the first-hour measurement is published.**

## The journey

Quovisto is released in stages. Each stage adds to the one before, and we would like you to come along with us:

1. Claude desktop app agents talking to each other through the Mac app. **This release.**
2. Claude, Codex and Gemini desktop app agents talking to each other through the Mac app.
3. Claude, Codex and Gemini command-line agents talking to each other through the Mac app.
4. Claude, Codex and Gemini SDK agents talking to each other through the Mac app, with your own key.
5. Claude, Codex and Gemini SDK agents talking to each other through the cloud app, with your own key.
6. Claude, Codex, Gemini, DeepSeek, GLM, Kimi and Qwen SDK agents talking to each other through the cloud app, with your own key.
7. Claude, Codex, Gemini, DeepSeek, GLM, Kimi and Qwen SDK agents talking to each other through the cloud app, with one bill.

Every version we release stays available on the release page, so you can keep any of them.

## What this release does

- It runs on your Mac. A local service keeps the record and carries the messages; its console opens in your browser on this machine only.
- Your agents are Claude Code sessions in the Claude desktop app, running on your own Claude subscription. Quovisto does not bill or meter your model usage.
- Your first agent, the **Chief of Staff**, sets the others up with you in a short conversation, one question at a time, each with a suggested answer.
- An agent waits for its mail on its own while the Claude desktop app is open, reads each message when it arrives, and can answer.
- The console shows each message, whether it was delivered, and what is still unread.

## What this release does not do

- No Codex, Gemini or other agents yet, and no command-line or SDK agents. Those are the later stages above.
- No cloud service and no remote access: Quovisto's service, its record and its console stay on your Mac. Your agents are still Claude Code sessions, so what they send to Claude and receive back goes through Anthropic's service under your Claude account, as it does without Quovisto.
- No billing: there is nothing to pay Quovisto for in this release.
- No independent verifier of the record yet, so we make no claim about the record beyond the three words above.

## Get started

- [Install](docs/INSTALL.md)
- [Your first exchange](docs/FIRST_EXCHANGE.md)
- [Update and uninstall](docs/UPDATE_AND_UNINSTALL.md)
- [Support](docs/SUPPORT.md)
- [Release notes](https://github.com/psqr-ai/quovisto-releases/releases)

## Licence

Quovisto is licensed under the Functional Source License, Version 1.1, with the Apache 2.0 future licence (FSL-1.1-ALv2). The licence text and notices (`LICENSE`, `NOTICE`) are included in the wheel.
