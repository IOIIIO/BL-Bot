import discord
from discord.ext import commands

class reeeport:
    """Report system for BL"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def report(self, ctx, *, message: str):
        server = self.bot.get_server(id="370628772489068565")
        member = ctx.message.author.id
        for member in server.members:
            em = discord.Embed(title="Report Case", description=message) 
            await self.bot.send_message(self.bot.get_channel(id="464926651218788353"), embed=em)
            await self.bot.send_message(self.bot.get_channel(id="464926651218788353"), '@here')
            await self.bot.say("Your report has been sent, the mods will look in to it as soon as possible.")
            break


def setup(bot):
    bot.add_cog(reeeport(bot))