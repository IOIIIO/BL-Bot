import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice
import os


class Compliment:

    """Based on the insult cog"""
    def __init__(self, bot):
        self.bot = bot
        self.compliments = fileIO("data/compliment/compliments.json","load")
        self.person = fileIO("data/compliment/self.json","load")

    @commands.command(pass_context=True, no_pm=True)
    async def compliment(self, ctx, user : discord.Member=None):
        """Compliment the user"""

        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = " Awww, thank you. That's so nice of you. I'll make sure to tell my makers!"
                await self.bot.say(user.mention + msg)
            elif user.id == ctx.message.author.id:
                await self.bot.say(ctx.message.author.mention + msg + randchoice(self.person))
            else:
                await self.bot.say(user.mention + msg + randchoice(self.compliments))
        else:
            await self.bot.say(ctx.message.author.mention + msg + randchoice(self.compliments))


def setup(bot):
    bot.add_cog(Compliment(bot))
