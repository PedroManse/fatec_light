import os
import discord
from discord.ext import tasks, commands
import subprocess
BOT_TOKEN = os.environ["BOT_TOKEN"]

FD_NULL = open(os.devnull, 'w')
CHAN_ID = 904490971365003297

def is_online():
    proc = subprocess.run(["ping", "-q", "-c1", "www.fatecsp.br"], stdout=FD_NULL)
    return proc.returncode == 0

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.online = True

    @tasks.loop(seconds=10)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(CHAN_ID)  # channel ID goes here
        on = is_online()
        if on != self.online:
            self.online = on
            await self.alert_change(channel)

    async def alert_change(self, channel):
        if self.online:
            await channel.send(f"Agr a FATEC está com energia")
        else:
            await channel.send(f"@everyone Agr a FATEC está **SEM** energia")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        channel = self.get_channel(CHAN_ID)  # channel ID goes here
        await channel.send("Bot está ligado")

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_message(self, message):
        # don't reply to own msgs
        if message.author.id == self.user.id: return;
        text = message.content
        if not text.startswith("!"): return;
        cmd, *args = text.split(" ")
        print(f"execute `{cmd}` with {args}")


    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents, command_prefix="!")
bot.run(BOT_TOKEN)
