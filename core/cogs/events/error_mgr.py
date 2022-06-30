import discord
from discord.ext import commands


class ErrorMgr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command \"{}\" not found".format(ctx.invoked_with))

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Command \"{}\" is on cooldown".format(ctx.invoked_with))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Missing permissions for command \"{}\"".format(ctx.invoked_with))

        elif isinstance(error, commands.MissingRole):
            await ctx.send("Missing role for command \"{}\"".format(ctx.invoked_with))

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments given for \"{}\"".format(ctx.invoked_with))

        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument(s) given for \"{}\"".format(ctx.invoked_with))

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument(s) for {}".format(ctx.invoked_with))

        else:
            await ctx.send("`{}`".format(ctx.invoked_with, error))





async def setup(bot):
    await bot.add_cog(ErrorMgr(bot))
