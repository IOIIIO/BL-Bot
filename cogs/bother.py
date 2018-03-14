from cogs.utils import checks
import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice
import os


class Marie:

    def __init__(self, bot):
        self.bot = bot
        self.bothers = fileIO("data/bother/bothers.json","load")
   
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_co()
    async def bother(self, ctx):
        """Bother the person"""

        msg = ' '
        await self.bot.say(msg + randchoice(self.bothers))


def setup(bot):
    bot.add_cog(Marie(bot))
