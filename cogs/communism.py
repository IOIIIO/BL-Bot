from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
from cogs.utils import checks
import os
import string


class communism:
    """This is so sad"""
    
    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/communism/communism.json", "load")
        self.exclude = fileIO("data/communism/exclude.json", "load")
        self.mute = fileIO("data/communism/users.json", "load")


    @commands.group(pass_context=True, no_pm=True)
    async def communism(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.admin_or_permissions(administrator=True)
    @communism.command(name="enable", no_pm=True, pass_context=True)
    async def _enable(self, ctx):
        """Execute this command if you want BL-Bot to respond to your filthy capitalism (administrators only)
If you execute it again, you will be switched back off."""
        self.settings = fileIO("data/communism/communism.json", "load")
        lserver = ctx.message.server.id
        if lserver in self.settings:
            self.settings.remove(lserver)
            fileIO("data/communism/communism.json", "save", self.settings)
            await self.bot.say("I will no longer respond")
        else:
            self.settings.append(lserver)
            fileIO("data/communism/communism.json", "save", self.settings)
            await self.bot.say("I will now respond!") 

    @checks.admin_or_permissions(administrator=True)
    @communism.command(name="exclude", pass_context=True, no_pm=True)
    async def _exclude(self, ctx, *, channel : str=None):
        """Execute this command if you don't want BL-Bot to respond to your filthy capitalism in this channel (administrators only)
If you execute it again, you will be switched back off."""
        self.exclude = fileIO("data/communism/exclude.json", "load")
        lchannel = None
        if channel != None:
            if '<#' in channel:
                lchannel = channel.replace('<#', '').replace('>', '')
            else:
                await self.bot.say("Channel not found")
                return
        else:
            lchannel = ctx.message.channel.id
        if lchannel in self.exclude:
            self.exclude.remove(lchannel)
            fileIO("data/communism/exclude.json", "save", self.exclude)
            await self.bot.say("I will respond again in this channel")
        else:
            self.exclude.append(lchannel)
            fileIO("data/communism/exclude.json", "save", self.exclude)
            await self.bot.say("I will no longer respond in this channel") 

    @communism.command(name="mute", no_pm=True, pass_context=True)
    async def _mute(self, ctx):
        """Execute this command if you want BL-Bot to respond to your filthy capitalism
If you execute it again, you will be switched back off."""
        self.mute = fileIO("data/communism/users.json", "load")
        luser = ctx.message.author.id
        if luser in self.mute:
            self.mute.remove(luser)
            fileIO("data/communism/users.json", "save", self.mute)
            await self.bot.say("I will now respond to you")
        else:
            self.mute.append(luser)
            fileIO("data/communism/users.json", "save", self.mute)
            await self.bot.say("I will no longer respond to you!")

    async def communize(self, text, channel): # Credits to CorpNewt for the improved communism 
        parts = text.replace("\t"," ").replace("\n"," ").split(" ")
        find  = ["your","yours","my","mine","his","hers","their","theirs","its"]
        exclude = ["he's","she's","it's","that's","what's","who's"]
        communist = ["OUR" if (x.lower() in find or x.lower().endswith("'s") and x.lower() not in exclude) else x for x in parts]
        if communist != parts :
            await self.bot.send_message(channel, " ".join(communist).rstrip(".,!?")+", comrade.")

    async def on_message(self, message):
        lserver = message.server.id
        channel = message.channel.id
        user = message.author.id
        self.settings = fileIO("data/communism/communism.json", "load")
        self.exclude = fileIO("data/communism/exclude.json", "load")
        self.mute = fileIO("data/communism/users.json", "load")
        if all([lserver in self.settings, channel not in self.exclude, user not in self.mute, message.author.bot == False]):
            await self.communize(str(message.content), message.channel)

def checks():
    if not os.path.exists('data/communism'):
        print('Creating data/communism folder...')
        os.makedirs('data/communism')
    if not dataIO.is_valid_json('data/communism/communism.json'):
        print('Creating data/communism/communism.json...')
        dataIO.save_json('data/communism/communism.json', [])
    if not dataIO.is_valid_json('data/communism/exclude.json'):
        print('Creating data/communism/exclude.json...')
        dataIO.save_json('data/communism/exclude.json', [])
    if not dataIO.is_valid_json('data/communism/users.json'):
        print('Creating data/communism/users.json...')
        dataIO.save_json('data/communism/users.json', [])

def setup(bot):
    checks()
    bot.add_cog(communism(bot))