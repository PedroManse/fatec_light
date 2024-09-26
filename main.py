import os
import discord
from discord.ext import tasks, commands
import pickle
import subprocess
import util


def store(file, info):
    with open(file, 'wb') as f:
        pickle.dump(info, f)

def load(file):
    try:
        with open(file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_active_chan(self):
        return bot.get_channel(ctx["active_chan_id"])

    def is_online(self) -> bool:
        proc = subprocess.run(["ping", "-q", "-c1", "www.fatecsp.br"], stdout=FD_NULL)
        return proc.returncode == 0

    @tasks.loop(seconds=10)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_active_chan()
        on = self.is_online()
        if on != ctx["online"]:
            ctx["online"] = on
            await self.alert_change(channel)

    async def alert_change(self, channel):
        com = "com" if ctx["online"] else "**SEM**"
        to_ping = ' '.join(ctx["pings"])
        await channel.send(f"Agr a FATEC está {com} energia\n{to_ping}")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        channel = self.get_channel(ctx["active_chan_id"])  # channel ID goes here
        if channel:
            await channel.send("Bot está ligado")

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_message(self, message):
        # don't reply to own msgs
        if message.author.id == self.user.id: return;
        text = message.content
        if not text.startswith("!"): return;
        await util.execute_command(self, message, text, ctx)
        store("bot_info.pkl", ctx)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

FD_NULL = open(os.devnull, 'w')
BOT_TOKEN = os.environ["BOT_TOKEN"]
ctx = load("bot_info.pkl") or {
    "active_chan_id": 0,
    "online":True,
    "pings": [],
}


intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents, command_prefix="!")
bot.run(BOT_TOKEN)
