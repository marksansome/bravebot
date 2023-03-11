# bravebot

A Discord bot for handling random/fun things

## Functionality

### Voice Chat Activity

Send messages about a server's voice channel activity. Every time a member connects, disconnects, or changes voice channels, notify about this.

- Messages are sent to a Discord server's [system channel](https://discordpy.readthedocs.io/en/stable/api.html#discord.Guild.system_channel). A system channel must be configured for this to function
- Messages are, optionally, sent to a slack channel if the `SLACK_WEBHOOK` environment variable is configured.
