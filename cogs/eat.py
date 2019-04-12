import os
from random import choice as randchoice
import discord
from discord.ext import commands
from cogs.utils.dataIO import fileIO
from .utils.chat_formatting import italics

class eat:
    """Remind the chat how dead it is"""
    
    def __init__(self, bot):
        self.bot = bot
        self.direct = "data/eat/eats.json"

    @commands.command(pass_context=True, no_pm=False, name='eat')
    async def _eat(self, context, *, victim : str=None):
        """Randomly chooses a way to eat."""
        server = context.message.server
        author = context.message.author
        db = fileIO(self.direct, "load")
        print(victim)
        if victim is not None:
            if "<@!" in victim or "<@" in victim:
                if "<@!" in victim:
                    user = victim.replace('<@!', '').replace('>', '')
                if "<@" in victim:
                    user = victim.replace('<@', '').replace('>', '')
                print(user)
                person = self.bot.get_member(user)
                print(person)
                print(person.id)
                print(person.display_name)
                if user == author.id:
                    message = str(randchoice(db["eat"]["self"]))
                elif user == self.bot.user.id:
                    message = str(randchoice(db["eat"]["bot"]))
                elif user != author.id and user != self.bot.user.id:
                    message = str(randchoice(db["eat"]["person"])).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
            elif "@everyone" in victim or "@here" in victim:
                await self.bot.say("Nice try funny guy")
            else:
                message = str(randchoice(db["eat"]["thing"])).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
        else:
            db = fileIO(self.direct, "load")
            message = str(randchoice(db["eat"]["nothing"]))
            await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)

def setup(bot):
    bot.add_cog(eat(bot))