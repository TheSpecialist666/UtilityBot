#!/home/pimpdaddy/.pyenv/versions/3.8.13/bin/python


import os
import sys
import json
import discord
from discord.ext import commands



# TODO: move this to __init__()
env_json = open(".env.json", "r")
env_data = json.load(env_json)

PREFIX = env_data["BOT_PREFIX"]
TOKEN = env_data["BOT_TOKEN"]
SERVER_ID = env_data["SERVER_ID"]





class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        # TODO: make pretty help command instead
        #help_cmd = commands.DefaultHelpCommand(
        #    no_category = "Commands"
        #)

        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Load event cogs
        for i in os.listdir("core/cogs/events"):
            if i.endswith(".py"):
                await self.load_extension(f"core.cogs.events.{i[:-3]}")

        # Load game command cogs
        for i in os.listdir("core/cogs/games/ClashRoyale"):
            if i.endswith(".py"):
                await self.load_extension(f"core.cogs.games.ClashRoyale.{i[:-3]}")

        for i in os.listdir("core/cogs/user"):
            if i.endswith(".py"):
                await self.load_extension(f"core.cogs.user.{i[:-3]}")

        # Works, but isn't needed just yet
        #for i in os.listdir("core/webhook/test"):
        #    if i.endswith(".py"):
        #        await self.load_extension(f"core.webhook.test.{i[:-3]}")



        # Sync tree
        await tree.sync(guild=discord.Object(id=SERVER_ID))




bot = Bot()
tree = bot.tree

try:
    bot.run(TOKEN)
except Exception as e:
    print("{}".format(e))
    sys.exit(-1)
