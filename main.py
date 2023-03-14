import discord
import os
import requests

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")

class BraveBot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            print(f"{message.author} pong", flush=True)
            await message.channel.send('pong')

    async def on_voice_state_update(self, member, before, after):
        guild = member.guild

        # do not send if there is no system channel in guild or if the member state change belongs to a bot user
        if guild.system_channel is None and member.bot:
            return

        # do not send if voice state change occurs in same channel. Eg. mute/unmute
        if before.channel is after.channel:
            return

        # disconnected
        if after.channel is None:
            to_send_mentions = f'{member.mention} has disconnected from {before.channel.mention}'
            to_send_names = f'{member.name} has disconnected from {before.channel.name}'
        # connected
        elif member in after.channel.members:
            # member is joing for first time
            if before.channel is None:
                to_send_mentions = f'{member.mention} has connected to {after.channel.mention}'
                to_send_names = f'{member.name} has connected to {after.channel.name}'
            # member is changing channels
            else:
                to_send_mentions = f'{member.mention} has changed channels from {before.channel.mention} to {after.channel.mention}'
                to_send_names = f'{member.name} has changed channels from {before.channel.name} to {after.channel.name}'

        # if the slack webhook exists, send a message to it
        if SLACK_WEBHOOK is not None or SLACK_WEBHOOK != "":
            requests.post(SLACK_WEBHOOK, json={"text": to_send_names})

        # Send message to Discord guild system channel
        await guild.system_channel.send(to_send_mentions)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = BraveBot(intents=intents)
client.run(DISCORD_BOT_TOKEN)
