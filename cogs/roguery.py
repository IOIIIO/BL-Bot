from discord.ext import commands


class roguery:
    """Remind the chat how dead it is"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ded(self, ctx):
        await self.bot.say("https://giphy.com/gifs/bare-barren-Az1CJ2MEjmsp2")


def setup(bot):
    bot.add_cog(roguery(bot))