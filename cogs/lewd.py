import os
import random
import discord
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
from random import choice as randchoice
from .utils.chat_formatting import italics


class Lewd:
    def __init__(self, bot):
        self.bot = bot
        self.cuddles = fileIO("data/lewd/cuddles.json","load")
        self.kisses = fileIO("data/lewd/kiss.json", "load")
        self.hold_self = fileIO("data/lewd/hand/self.json","load")
        self.hold_person = fileIO("data/lewd/hand/person.json","load")
        self.hold_nothing = fileIO("data/lewd/hand/nothing.json","load")
        self.hug_list = fileIO("data/lewd/hug.json", "load")
        self.hug_gifs = fileIO("data/lewd/gifs.json", "load")

    @commands.command(pass_context=True, no_pm=False)
    async def handhold(self, ctx, user : discord.Member=None):
        """Hold another users hand."""
        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = " You try to hold the bots hand, only then you realise computers don't have hands."
                await self.bot.say(user.display_name + msg)
            elif user.id == ctx.message.author.id:
                await self.bot.say(randchoice(self.hold_self).format(victim=user.display_name, holder=ctx.message.author.display_name))
            else:
                await self.bot.say(randchoice(self.hold_person).format(victim=user.display_name, holder=ctx.message.author.display_name))
        elif user is None:
            await self.bot.say("You try to hold hands with air.")
        else:
            await self.bot.say(randchoice(self.hold_person).format(victim=user.display_name, holder=ctx.message.author.display_name))

    @commands.command(pass_context=True, no_pm=False)
    async def cuddle(self, ctx, user : discord.Member=None):
        """Cuddles the user. Messages brought to you by @Mandelora#1108"""
        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = " You try to cuddle the bot but end up hugging a metal box."
                await self.bot.say(user.mention + msg)
            elif user.id == ctx.message.author.id:
                user = ctx.message.author
                msg = " You wrap your arms around yourself."
                await self.bot.say(user.mention + msg)
            else:
                await self.bot.say(randchoice(self.cuddles).format(victim=user.display_name, cuddler=ctx.message.author.display_name))
        elif user is None:
            await self.bot.say("You try to cuddle with air.")
        else:
            await self.bot.say(randchoice(self.cuddles).format(victim=user.display_name, cuddler=ctx.message.author.display_name))

    @commands.command(pass_context=True, no_pm=False)
    async def kiss(self, ctx, user : discord.Member=None):
        """Kiss the user."""
        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = " You give a nice kiss to a metal box in some kid's room."
                await self.bot.say(user.mention + msg)
            else:
                await self.bot.say(randchoice(self.kisses).format(victim=user.display_name, kisser=ctx.message.author.display_name))
        elif user is None:
            await self.bot.say("You try to kiss the air.")
        else:
            await self.bot.say(randchoice(self.kisses).format(victim=user.display_name, kisser=ctx.message.author.display_name))
        

    #@commands.command(no_pm=True, hidden=True)
    #async def hug(self, user : discord.Member, intensity : int=1):
    #    """Because everyone likes hugs
    #
    #    Up to 10 intensity levels."""
    #    name = italics(user.display_name)
    #    if intensity <= 0:
    #        msg = "(っ˘̩╭╮˘̩)っ" + name
    #    elif intensity <= 3:
    #        msg = "(っ´▽｀)っ" + name
    #    elif intensity <= 6:
    #        msg = "╰(*´︶`*)╯" + name
    #    elif intensity <= 9:
    #        msg = "(つ≧▽≦)つ" + name
    #    elif intensity >= 10:
    #        msg = "(づ￣ ³￣)づ{} ⊂(´・ω・｀⊂)".format(name)
    #    await self.bot.say(msg)

    @commands.command(no_pm=True, pass_context=True)
    async def hug(self, ctx, user : discord.Member, intensity : str=None):
        """Because everyone likes hugs"""
  
        self.hug_list = fileIO("data/lewd/hug.json", "load")      
        if ctx.message.server.id not in self.hug_list:
            state = random.getstate()
            num = random.randint(1, 16)
            random.setstate(state)
            channel = ctx.message.channel
            #msg = 'data/lewd/hugs/{}.gif'.format(num)
            msg2 = "*{hugger}* pulls *{hugged}* in for a hug.".format(hugger=ctx.message.author.display_name, hugged=user.display_name)
            #await self.bot.send_file(channel, msg)
            #await self.bot.say(msg2)
            em = discord.Embed(color=discord.Color.green(), title=msg2)
            em.set_image(url=randchoice(self.hug_gifs))
            await self.bot.send_message(ctx.message.channel, embed = em)
            

        else:
            name = italics(user.display_name)
            if intensity is None:
                msg = "(っ´▽｀)っ" + name
            else:
                if intensity.isdigit() == True:
                    intensity = float(intensity)
                    if intensity <= 0:
                        msg = "(っ˘̩╭╮˘̩)っ" + name
                    elif intensity <= 3:
                        msg = "(っ´▽｀)っ" + name
                    elif intensity <= 6:
                        msg = "╰(*´︶`*)╯" + name
                    elif intensity <= 9:
                        msg = "(つ≧▽≦)つ" + name
                    elif intensity >= 10:
                        msg = "(づ￣ ³￣)づ{} ⊂(´・ω・｀⊂)".format(name)
                else:
                    msg = "(っ´▽｀)っ" + name
            await self.bot.say(msg)

    @checks.admin_or_permissions(administrator=True)
    @commands.command(no_pm=True, pass_context=True)
    async def optout(self, ctx):
        """Execute this command if you want to go back to the old hug style (administrators only)
If you execute it again, you will be switched back to the new style."""
        server = ctx.message.server.id
        if server in self.hug_list:
            self.hug_list.remove(server)
            fileIO("data/lewd/hug.json", "save", self.hug_list)
            await self.bot.say("I will be using the new hug style on this server!")
        else:
            self.hug_list.append(server)
            fileIO("data/lewd/hug.json", "save", self.hug_list)
            await self.bot.say("I will be using the old hug style on this server!") 

    @commands.command()
    async def gay(self, *, user : discord.Member):
        """Detects how gay a person is

        This is 100% accurate."""
        state = random.getstate()
        random.seed(user.id)
        percent = random.randint(0, 101)
        if str(user.id) == '263497047800283156':
            percent = 10000000
        if percent == 0:
            amount = "not at all"
        elif percent < 10:
            amount = "barely"
        elif percent < 26:
            amount = "kinda"
        elif percent < 41:
            amount = "somewhat"
        elif percent < 51:
            amount = "half"
        elif percent < 76:
            amount = "pretty"
        elif percent < 91:
            amount = "hella"
        elif percent < 101:
            amount = "totally"
        else:
            amount = "off the charts"
        message = """*{gay}* is {cent}% gay
That is {how} gay.""".format(gay=user.display_name, cent=percent, how=amount)
        random.setstate(state)
        await self.bot.say(message)

def checks():
    if not os.path.exists('data/lewd'):
        print('Creating data/lewd folder...')
        os.makedirs('data/lewd')
    if not dataIO.is_valid_json('data/lewd/cuddles.json'):
        print('Creating data/lewd/cuddles.json...')
        dataIO.save_json('data/lewd/cuddles.json', {})
    if not os.path.exists('data/lewd/hand'):
        print('Creating data/lewd/hand folder...')
    if not dataIO.is_valid_json('data/lewd/hand/person.json'):
        print('Creating default person.json...')
        dataIO.save_json('data/lewd/hand/person.json', {})
    if not dataIO.is_valid_json('data/lewd/hand/self.json'):
        print('Creating default self.json...')
        dataIO.save_json('data/lewd/hand/self.json', {})
    if not dataIO.is_valid_json('data/lewd/hand/nothing.json'):
        print('Creating default nothing.json...')
        dataIO.save_json('data/lewd/hand/nothing.json', {})
    if not dataIO.is_valid_json('data/lewd/hug.json'):
        print('Creating default hug.json...')
        dataIO.save_json('data/lewd/hug.json', [])

def check_folders():
    folders = ('data', 'data/lewd', '/data/lewd/hugs')
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)

def setup(bot):
    checks()
    check_folders()
    bot.add_cog(Lewd(bot))
