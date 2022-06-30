import json
import discord
import requests
from pathlib import Path
from discord.ext import commands



class PlayerMgr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.null_icon = "https://i.imgur.com/Y3uXsgj.png"
        self.img_url = "https://cdn3.emoji.gg/emojis/2250_clash_royale.png"

        # Get API token
        with open("core/data/games/ClashRoyale/api/api_token.json", "r") as f:
            token = json.load(f)
            self.api_token = token["CR_API_TOKEN"]
            f.close()



    @commands.group(name="cr_user_mgr")
    async def player_mgr(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Usage: <prefix>cr_user_mgr <cmd> <args>\n\n"
            )
            return

    @player_mgr.command(
        name="get_chest_stats",
        aliases=["gc", "-gc", "--get-chest"]
    )
    async def get_chest_cmd(self, ctx: commands.Context, tag: str = None):
        if tag == None:
            await ctx.send(
                "Hey {}! You must provide a player tag!".format(ctx.author.mention)
            )
            return

        # Strip "#" from tag if it's found
        if tag.startswith("#"):
            tag = tag.replace("#", "")


        header = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(self.api_token)
        }
        req = requests.request(
            "GET",
            f"https://proxy.royaleapi.dev/v1/players/%23{tag}/upcomingchests",
            headers=header
        )

        # Check status code
        if req.status_code != 200:
            await ctx.send(
                "Hey {} I got error `{}` trying to access this tag".format(ctx.author.mention, req.status_code)
            )
        else:
            # Get raw json contents
            raw = req.json()


        # Because this data is small... We can use a single embed
        # but this embed doesn't need a title or description
        ch_eb = discord.Embed(
            title="*Upcoming chest stats*",
            description="",
            color=discord.Color.red()
        )

        # This current URL used was from:
        # https://emoji.gg/emojis/clash
        ch_eb.set_thumbnail(
            url="{}".format(self.img_url)
        )

        # Contruct embed containing chest details. This won't be sexy either
        # so don't get too excited
        for i in raw["items"]:
            if i["index"] == "0" or i["index"] == 0:
                ch_eb.add_field(
                    name="*Next chest*",
                    value="{}".format(i["name"]),
                    inline=False
                )

            else:
                ch_eb.add_field(
                    name="*Upcoming:\n{}*".format(i["name"]),
                    value=" +{} until next chest".format(i["index"]),
                    inline=True
                )


        await ctx.send(embed=ch_eb)



async def setup(bot):
    await bot.add_cog(PlayerMgr(bot))
