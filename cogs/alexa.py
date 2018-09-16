from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
from cogs.utils import checks
import os


class alexa:
    """This is so sad"""
    
    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/alexa/alexa.json", "load")
        self.exclude = fileIO("data/alexa/exclude.json", "load")


    @commands.group(pass_context=True, no_pm=True)
    async def alexa(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.admin_or_permissions(administrator=True)
    @alexa.command(name="enable", no_pm=True, pass_context=True)
    async def enable(self, ctx):
        """Execute this command if you want BL-Bot to respond to your sadness (administrators only)
If you execute it again, you will be switched back."""
        self.settings = fileIO("data/alexa/alexa.json", "load")
        lserver = ctx.message.server.id
        if lserver in self.settings:
            self.settings.remove(lserver)
            fileIO("data/alexa/alexa.json", "save", self.settings)
            await self.bot.say("I will no longer resond")
        else:
            self.settings.append(lserver)
            fileIO("data/alexa/alexa.json", "save", self.settings)
            await self.bot.say("I will now respond!") 

    @checks.admin_or_permissions(administrator=True)
    @alexa.command(name="exclude", pass_context=True, no_pm=True)
    async def _exclude(self, ctx, *, channel : str=None):
        """Execute this command if you don't want BL-Bot to respond to your sadness in this channel (administrators only)
If you execute it again, you will be switched back."""
        self.exclude = fileIO("data/alexa/exclude.json", "load")
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
            fileIO("data/alexa/exclude.json", "save", self.exclude)
            await self.bot.say("I will respond again in this channel")
        else:
            self.exclude.append(lchannel)
            fileIO("data/alexa/exclude.json", "save", self.exclude)
            await self.bot.say("I will no longer respond in this channel") 

    async def on_message(self, message):
        lserver = message.server.id
        channel = message.channel.id
        self.settings = fileIO("data/alexa/alexa.json", "load")
        self.exclude = fileIO("data/alexa/exclude.json", "load")
        if lserver in self.settings:
            if channel not in self.exclude:
                if "this is so sad" in message.content.lower():
                    await self.bot.send_message(message.channel, 'Alexa play Despacito \nhttps://www.youtube.com/watch?v=kJQP7kiw5Fk')
            else:
                return
        else: 
            return
            

def checks():
    if not os.path.exists('data/alexa'):
        print('Creating data/alexa folder...')
        os.makedirs('data/alexa')
    if not dataIO.is_valid_json('data/alexa/alexa.json'):
        print('Creating data/alexa/alexa.json...')
        dataIO.save_json('data/alexa/alexa.json', [])
    if not dataIO.is_valid_json('data/alexa/exclude.json'):
        print('Creating data/alexa/exclude.json...')
        dataIO.save_json('data/alexa/exclude.json', [])

def setup(bot):
    checks()
    bot.add_cog(alexa(bot))