from discord.ext import commands


class roguery2:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ded(self, ctx):
        await self.bot.send_file('../data/ded/ded.gif')


def setup(bot):
    bot.add_cog(roguery2(bot))