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


    @commands.group(pass_context=True, no_pm=True)
    async def communism(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.admin_or_permissions(administrator=True)
    @communism.command(name="enable", no_pm=True, pass_context=True)
    async def enable(self, ctx):
        """Execute this command if you want BL-Bot to respond to your filthy capitalism (administrators only)
If you execute it again, you will be switched back off."""
        self.settings = fileIO("data/communism/communism.json", "load")
        lserver = ctx.message.server.id
        if lserver in self.settings:
            self.settings.remove(lserver)
            fileIO("data/communism/communism.json", "save", self.settings)
            await self.bot.say("I will no longer resond")
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

    async def on_message(self, message):
        lserver = message.server.id
        channel = message.channel.id
        self.settings = fileIO("data/communism/communism.json", "load")
        self.exclude = fileIO("data/communism/exclude.json", "load")
        if lserver in self.settings:
            if channel not in self.exclude:
                if message.author != self.bot.user:
                    if find_substring("your", message.content.lower()):
                        answer = message.content.lower().split("your")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                    elif find_substring("yours", message.content.lower()):
                        answer = message.content.lower().split("yours")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                    elif find_substring("my", message.content.lower()):
                        answer = message.content.lower().split("my")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                    elif find_substring("mine", message.content.lower()):
                        answer = message.content.lower().split("mine")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                    elif find_substring("his", message.content.lower()):
                        answer = message.content.lower().split("his")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                    elif find_substring("hers", message.content.lower()):
                        answer = message.content.lower().split("hers")[1]
                        await self.bot.send_message(message.channel, "our" + answer)
                else:
                    return
            else:
                return
        else: 
            return
            

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

def find_substring(needle, haystack): # credits to aronasterling on Stack Overflow
    index = haystack.find(needle)
    if index == -1:
        return False
    if index != 0 and haystack[index-1] not in string.whitespace:
        return False
    L = index + len(needle)
    if L < len(haystack) and haystack[L] not in string.whitespace:
        return False
    return True

def setup(bot):
    checks()
    bot.add_cog(communism(bot))