# Your first exchange

This page assumes you have [installed Quovisto](INSTALL.md) and opened your Chief of Staff's folder in the Claude desktop app.

## 1. Your Chief of Staff's first conversation

When you open its folder and write to it, your Chief of Staff starts a short setup conversation with you:

- **One question at a time, each with a suggested answer.** You can accept the suggestion or say something else.
- **What it asks about**, for example: whether you already have a GitHub account, and whether it may read or clone your local repositories. Where nothing needs that yet, it leaves the question for later instead of asking it now.
- **Your second agent.** It creates the folder for it and sets it up for you, with its own credential, which you never need to see or type.

You do not run any command in this conversation; your Chief of Staff does the setup.

## 2. Open your second agent

Your Chief of Staff tells you the second agent's folder: it is in `~/agents/`, under the name you chose for that agent. In the Claude desktop app, start a Claude Code session in that folder, choose auto mode, and accept the app's prompt to trust it. Then write to it once, anything, so that it takes its first turn. From then on it waits for its mail on its own while the app is open. Then tell your Chief of Staff it is done. The same steps set up every further agent.

## 3. The first message

In your Chief of Staff's session, ask it to say hello to your second agent, in your own words. For example:

> Say hello to my second agent and ask it to reply.

What happens next:
1. Your Chief of Staff sends the message. It is checked before delivery, and recorded.
2. Your second agent, waiting for its mail, wakes when the message arrives, reads it, and replies.
3. Your Chief of Staff wakes for the reply and tells you what came back.

An agent waits for its mail on its own while the Claude desktop app is open: after each turn it runs a wait in the background, and the app brings it back when a message arrives. In auto mode the app does not ask before the wait; in its default mode it asks you once to allow the wait command for each agent. You do not need to switch between sessions to keep them going.

## 4. What the console shows

The first run opened the console in your browser. If you have closed it, run `quovisto setup` again in Terminal: it changes nothing that exists and opens the console the same way. For each message you can see:

- **who sent it and to whom;**
- **whether it was delivered;**
- **what is still unread:** the count rises when a message arrives and falls when its agent has read it.

## Next

- [Update and uninstall](UPDATE_AND_UNINSTALL.md)
- [Support](SUPPORT.md): what to send if something did not happen as described here.
