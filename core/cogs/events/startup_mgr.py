import discord
from discord.ext import commands
from datetime import datetime as dt


class StartupMgr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Discord API version (Python): {}".format(discord.__version__))
        print("Bot: {}".format(self.bot.user))
        print("Bot ID: {}".format(self.bot.user.id))



async def setup(bot):
    await bot.add_cog(StartupMgr(bot))
