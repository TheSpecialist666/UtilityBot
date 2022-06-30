import discord
from asyncio import sleep
from discord.ext import commands





class Dropdown(discord.ui.Select):
    def __init__(self):
        # Options list
        opt_list = [
            discord.SelectOption(label="Test1", description="Testing drop down")
        ]




class ThreadMgr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.add_view(TestView())


    @commands.command(
        name="test"
    )
    async def test_cmd(self, ctx: commands.Context):
        # Clean called command and prefix
        #await ctx.message.delete()

        # Check if we're in the proper help thread
        channel = ctx.channel
        #if channel.name != "test-help":
        #    await ctx.send(
        #        "Woah {} you must be in a proper help channel to use this command!".format(ctx.author.mention)
        #    )
        #    return
        #else:
        #    await channel.typing()

        # Create new channel thread
        thread = await ctx.channel.create_thread(
            name="Test Thread",
            type=discord.ChannelType.public_thread,
        )

        # Don't allow non-moderators to add other non-moderators to
        # any help thread made for the user
        await thread.edit(
            invitable=false
        )

        thread_eb = discord.Embed(
            title="User reporter",
            description="Fill out form below for user to be reported. This will be send to the server"
                        "moderators/administrators for further review",
            color=discord.Color.green()
        )


        await thread.send(
            content="Welcome {} to {}!".format(ctx.author.name, thread.name),
            embed=thread_eb,
        )


        #await sleep(15.0)

        # Wait for report to be submitted before closing the thread. It may be better to also
        # have the bot close the thread upon user input (calles the close command via prefix)
        #await thread.delete()

        # After thread deletion make sure we clean up any left over
        # messages from the bot and user
        #await channel.delete_messages([discord.Object(id=thread.id)])







async def setup(bot):
    await bot.add_cog(ThreadMgr(bot))
