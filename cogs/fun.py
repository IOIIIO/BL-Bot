from discord.ext import commands


class fun:
    """Random fun commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        await self.bot.say("https://cataas.com/cat/gif")


def setup(bot):
    bot.add_cog(fun(bot))