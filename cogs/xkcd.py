from discord.ext import commands
import discord
import json
import urllib.request

class XKCD:
    def __init__(self, bot):
        self.bot = bot
        self.apiurl = "http://xkcd.com/{x}/info.0.json"
        self.current = "http://xkcd.com/info.0.json"

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, number: int=None):
        if number is None: 
            with urllib.request.urlopen(self.current) as url:
                data = json.loads(url.read().decode())
                em = discord.Embed(title=data["title"], description="Alt: {x}".format(x = data["alt"], color=discord.Color.red()))
                em.set_image(url=data["img"])
                em.set_footer(text="XKCD nr.{}".format(data["num"]))
                await self.bot.say(embed = em)
        else:
            try:
                with urllib.request.urlopen(self.apiurl.format(x = number)) as url:
                    data = json.loads(url.read().decode())
                    em = discord.Embed(title=data["title"], description="Alt: {x}".format(x = data["alt"], color=discord.Color.red()))
                    em.set_image(url=data["img"])
                    em.set_footer(text="XKCD nr.{}".format(data["num"]))
                    await self.bot.say(embed = em)
            except:
                await self.bot.say("Could not find an XKCD with this ID!")
                
def setup(bot):
    bot.add_cog(XKCD(bot))
