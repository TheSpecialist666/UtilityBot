import json
import discord
import requests
from discord.ext import commands




class ClanMgr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.null_icon = "https://i.imgur.com/Y3uXsgj.png"
        self.img_url = "https://cdn3.emoji.gg/emojis/2250_clash_royale.png"

        # Get API token
        with open("core/data/games/ClashRoyale/api/api_token.json", "r") as f:
            token = json.load(f)
            self.api_token = token["CR_API_TOKEN"]
            f.close()



    @commands.group(name="cr_clan_mgr")
    async def clan_mgr(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Usage: <prefix>cr_clan_mgr <cmd> <args>\n\n"
                "- search_clan (aliases sc, -sc, --search-clan) search clan profile via tag\n"
                "  usage: <prefix>clan_mgr -sc <tag>\n\n"
            )
            return

    @clan_mgr.command(
        name="search_clan",
        aliases=["sc", "-sc", "--search-clan"]
    )
    async def search_cmd(self, ctx: commands.Context, tag: str = None):
        if tag == None:
            await ctx.send(
                "Hey there {}! You need to provide a clan tag!".format(ctx.author.mention)
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
            f"https://proxy.royaleapi.dev/v1/clans/%23{tag}",
            headers=header
        )

        # Check status code
        if req.status_code != 200:
            await ctx.send(
                "Hey {} I got error {} trying to access this tag".format(ctx.author.mention, req.status_code)
            )
        else:
            # Get raw json contents
            raw = req.json()


        clan_eb = discord.Embed(
            title="*Clan stats*",
            description="",
            color=discord.Color.green()
        )

        clan_eb.set_thumbnail(
            url="{}".format(self.img_url)
        )

        clan_eb.add_field(
            name="*Clan*",
            value="{}".format(raw["name"]),
            inline=True
        )

        clan_eb.add_field(
            name="*Clan type*",
            value="{}".format(raw["type"]),
            inline=True
        )

        clan_eb.add_field(
            name="*Clan description*",
            value="{}".format(raw["description"]),
            inline=False
        )

        clan_eb.add_field(
            name="*Clan score*",
            value="{}".format(raw["clanScore"]),
            inline=True
        )

        clan_eb.add_field(
            name="*Clan war trophies*",
            value="{}".format(raw["clanWarTrophies"]),
            inline=True
        )

        clan_eb.add_field(
            name="*Required trophies*",
            value="{}".format(raw["requiredTrophies"]),
            inline=True
        )

        clan_eb.add_field(
            name="*Members*",
            value="{}".format(raw["members"]),
            inline=False
        )

        # NOTE: embeds have a field limit of 25...
        for i in raw["memberList"]:
            clan_eb.add_field(
                name="*{}*".format(i["name"]),
                value="Tag: {}\n"
                      "Role: {}\n"
                      "Level: {}\n"
                      "Trophies: {}\n"
                      "Arena: {}\n"
                      "Donations: {}\n"
                      "Donations received: {}\n".format(i["tag"], i["role"], i["expLevel"], i["trophies"], i["arena"]["name"], i["donations"], i["donationsReceived"])
            )
        await ctx.send(embed=clan_eb)










async def setup(bot):
    await bot.add_cog(ClanMgr(bot))
