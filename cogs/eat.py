import os
import random
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.chat_formatting import italics


class Eat:
    def __init__(self, bot):
        self.bot = bot
        #self.user = ctx.message.author

        self.eat_nothing = []
        self.eat_nothing.append('you sit quietly and eat *nothing*...')
        self.eat_nothing.append('you\'re *sure* there was something to eat, so you just chew on nothingness...')
        self.eat_nothing.append('there comes a time when you need to realize that you\'re just chewing nothing for the sake of chewing.  That time is now.')

        self.eat_self = []
        self.eat_self.append('you clamp down on your own forearm - not surprisingly, it hurts.')
        self.eat_self.append('you place a finger into your mouth, but *just can\'t* force yourself to bite down.')
        self.eat_self.append('you happily munch away, but can now only wave with your left hand.')
        self.eat_self.append('wait - you\'re not a sandwich!')
        self.eat_self.append('you might not be the smartest...')

        self.eat_bot = []
        self.eat_bot.append('you try to eat *me* - but unfortunately, I saw it coming - your jaw hangs open as I deftly sidestep.')
        self.eat_bot.append('your mouth hangs open for a brief second before you realize that *I\'m* eating *you*.')
        self.eat_bot.append('I\'m a bot. You can\'t eat me.')
        self.eat_bot.append('your jaw clamps down on... wait... on nothing, because I\'m *digital!*.')
        self.eat_bot.append('what kind of bot would I be if I let you eat me?')
        
        self.eat_person = []
        self.eat_person.append('you unhinge your jaw and consume *{victim}* in one bite.')
        self.eat_person.append('you try to eat *{victim}*, but you just can\'t quite do it - you spit them out, the taste of failure hanging in your mouth...')
        self.eat_person.append('you take a quick bite out of *{victim}*.  They probably didn\'t even notice.')
        self.eat_person.append('you sink your teeth into *{victim}\'s* shoulder - they turn to face you, eyes wide as you try your best to scurry away and hide.')
        self.eat_person.append('your jaw clamps down on *{victim}* - a satisfying *crunch* emanates as you finish your newest meal.')

    @commands.command(pass_context=True, no_pm=False, name='eat')
    async def _eat(self, context, victim: discord.Member):
        """Randomly chooses a way to eat."""
        server = context.message.server
        author = context.message.author
        if victim.id == "":
            message = str(random.choice(self.eat_nothing))
        elif victim.id == author.id:
            message = str(random.choice(self.eat_self))
        elif victim.id == self.bot.user.id:
            message = str(random.choice(self.eat_bot))
        elif victim.id != "" and victim.id != author.id and victim.id != self.bot.user.id:
            message = str(random.choice(self.eat_person)).format(victim=victim.display_name)
        await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)


def setup(bot):
    bot.add_cog(Eat(bot))