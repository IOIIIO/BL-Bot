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

        self.drink_nothing = []
        self.drink_nothing.append('you stare at your glass full of *nothing*...')
        self.drink_nothing.append('that cup must\'ve had something in it, so you drink *nothing*...')
        self.drink_nothing.append('you should probably just go get a drink.')

        self.drink_self = []
        self.drink_self.append('you stab yourself with a straw - not surprisingly, it hurts.')
        self.drink_self.append('you fit yourself in to a cup, but you just can\'t do it.')
        self.drink_self.append('you happily drink away, but you are now very floppy.')
        self.drink_self.append('wait - you\'re not a drink!')
        self.drink_self.append('you might not be the smartest...')

        self.drinkeat_bot = []
        self.drinkeat_bot.append('you try to drink *me*, but I dodge your straw.')
        self.drinkeat_bot.append('You search for me, only to realise that *I* am already drinking you!')
        self.drinkeat_bot.append('I\'m a bot.  You can\'t drink me.')
        self.drinkeat_bot.append('you stick a straw in... wait... in nothing, because I\'m *digital!*.')
        self.drinkeat_bot.append('what do you think I am to let you drink me?')
        
        self.drink_person = []
        self.drink_person.append('you grab your lucky straw and empty *{victim}* in one sip.')
        self.drink_person.append('you try to drink *{victim}*, but you just can\'t quite do it - you spit them out, the taste of failure hanging in your mouth...')
        self.drink_person.append('you drink a small sip of *{victim}*.  They probably didn\'t even notice.')
        self.drink_person.append('you stab your straw into *{victim}\'s* shoulder - You run away as they run after you.')
        self.drink_person.append('you happily drink away - *{victim}* starts to look like an empty Capri Sun package.')

        self.drink_thing = []
        self.drink_thing.append('you take a big sip of *{victim}*. *Delicious.*')
        self.drink_thing.append('your straw sinks into *{victim}* - it tastes satisfying.')
        self.drink_thing.append('you thirstly guzzle *{victim}*, it\'s lovely!')
        self.drink_thing.append('you just can\'t bring yourself to drink *{victim}* - so you just hold it for awhile...')
        self.drink_thing.append('you attempt to drain *{victim}*, but you\'re clumsier than you remember - and fail...')



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

        self.eat_thing = []
        self.eat_thing.append('you take a big chunk out of *{victim}*. *Delicious.*')
        self.eat_thing.append('your teeth sink into *{victim}* - it tastes satisfying.')
        self.eat_thing.append('you rip hungrily into *{victim}*, tearing it to bits!')
        self.eat_thing.append('you just can\'t bring yourself to eat *{victim}* - so you just hold it for awhile...')
        self.eat_thing.append('you attempt to bite into *{victim}*, but you\'re clumsier than you remember - and fail...')

    @commands.command(pass_context=True, no_pm=False, name='eat')
    async def _eat(self, context, *, victim =None):
        """Randomly chooses a way to eat."""
        server = context.message.server
        author = context.message.author
        if victim is not None:
            if "<@!" in victim or "<@" in victim:
                if "<@!" in victim:
                    user = victim.replace('<@!', '').replace('>', '')
                if "<@" in victim:
                    user = victim.replace('<@', '').replace('>', '')
                person = self.bot.get_user_info(user)
                if user == author.id:
                    message = str(random.choice(self.eat_self))
                elif user == self.bot.user.id:
                    message = str(random.choice(self.eat_bot))
                elif user != author.id and user != self.bot.user.id:
                    message = str(random.choice(self.eat_person)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
            elif "@everyone" in victim or "@here" in victim:
                await self.bot.say("Nice try funny guy")
            else:
                message = str(random.choice(self.eat_thing)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
        else:
            message = str(random.choice(self.eat_nothing))
            await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)

    @commands.command(pass_context=True, no_pm=False, name='drink')
    async def _drink(self, context, *, victim =None):
        """Randomly chooses a way to drink."""
        server = context.message.server
        author = context.message.author
        if victim is not None:
            if "<@!" in victim or "<@" in victim:
                if "<@!" in victim:
                    user = victim.replace('<@!', '').replace('>', '')
                if "<@" in victim:
                    user = victim.replace('<@', '').replace('>', '')
                person = self.bot.get_user_info(user)
                if user == author.id:
                    message = str(random.choice(self.drink_self))
                elif user == self.bot.user.id:
                    message = str(random.choice(self.drink_bot))
                elif user != author.id and user != self.bot.user.id:
                    message = str(random.choice(self.drink_person)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
            elif "@everyone" in victim or "@here" in victim:
                await self.bot.say("Nice try funny guy")
            else:
                message = str(random.choice(self.drink_thing)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
        else:
            message = str(random.choice(self.drink_nothing))
            await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)

        



def setup(bot):
    bot.add_cog(Eat(bot))