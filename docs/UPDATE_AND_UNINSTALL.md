# Update and uninstall

## Update

Every version stays on the release page with its own files and hashes. A version is never replaced; a newer one is added beside it.

To move to a newer version:

1. Stop the local service:
   ```sh
   quovisto down
   ```
2. Run the install line from that version's install page. It checks and installs the newer wheel over the installed one, then runs `quovisto setup`, which starts the service again.

- **To check the file by hand first,** follow that version's install page: the check comes before the install.
- **Your record is kept.** `quovisto down` stops the local service and leaves your messages and history in place; the first run starts it again on the same record.
- **Your agents' sessions are not restarted**, and an update does not change your agents' folders. If a version needs something done in them, its release notes say so.

To go back to an earlier version, do the same with that version's install line. Every version stays on the [release page](https://github.com/psqr-ai/quovisto-releases/releases).

## Uninstall

```sh
quovisto down
uv tool uninstall quovisto
```

This removes the program and leaves your data where it is:

- **Your record** stays in `~/.quovisto`.
- **Your agents' folders** stay where they were created, in `~/agents/`.

To remove everything, delete `~/.quovisto` and your agents' folders yourself. **That cannot be undone:** your record goes with them. Keep a copy first if you may want it later.
