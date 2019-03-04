import discord, os, random
from discord.ext import commands
from cogs.utils import checks
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from cogs.utils.dataIO import fileIO

def check_file(): #Check if the json exists
    f = 'data/images/allowed.json'
    if not fileIO(f, 'check'):
        print('Creating empty allowed.json...')
        fileIO(f, 'save', {})
        
def check_file2(): #Check if the json exists
    g = 'data/images/cache.json'
    if not fileIO(g, 'check'):
        print('Creating empty cache.json...')
        fileIO(g, 'save', {})


def setup(bot):
    check_file()
    check_file2()
    bot.add_cog(cockschelle(bot))

class cockschelle:

    def __init__(self, bot):
        self.bot = bot
        #self.height = 0
        self.direct = "data/images/allowed.json"
        self.cache = "data/images/cache.json"
        self.od = "551920404642398238" #Cache channel ID

    @checks.admin_or_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def allowschelle(self, ctx, chan:discord.Channel):
        """Enable cockschelle in a channel. This locks it in all other channels."""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if server.id not in db:
            db[server.id] = [] #Black magic
            fileIO(self.direct, "save", db)
        if chan.id in db[server.id]:
            db[server.id].remove(chan.id)
            fileIO(self.direct, "save", db) #Remove servers from list
            await self.bot.say("Channel removed from the list")
        elif chan.id not in db[server.id]:
            db[server.id].append(chan.id)
            fileIO(self.direct, "save", db)
            await self.bot.say("Channel added to the list")    


    @commands.command(aliases=["cockslap"], pass_context=True)
    async def cockschelle(self, ctx, person: discord.Member):
        """KELLER ODER COCKSCHELLE"""

        self.person = person
        self.message = ctx.message
        db = fileIO(self.direct, "load")
        if ctx.message.server.id in db:
            if ctx.message.channel.id not in db[ctx.message.server.id]: #Check if the command is allowed in this channel
                await self.bot.say("Command not allowed in this channel.")
            else:     
                db = fileIO(self.cache, "load")
                if person.avatar_url not in db:
                    db[person.avatar_url] = [] #Same black magic
                    fileIO(self.cache, "save", db)
                if len(db[person.avatar_url]) == 0: #Check if there is a URL cached for this pfp, in this case: Not cached
                    server = ctx.message.channel
                    pic_ext = ['.jpg','.png','.jpeg']
                    self.person = person
                    self.message = ctx.message

                    fg = Image.open("data/images/slap.png")
                    temp = Image.open("data/images/temp.png")
                    pfp = person.avatar_url
                    response = requests.get(pfp)
                    bg = Image.open(BytesIO(response.content)) #Load the pfp as bg
                    bg = bg.convert('RGBA')

                    basewidth = 356
                    wpercent = (basewidth/float(bg.size[0]))
                    hsize = int((float(bg.size[1]) * float(wpercent))) 
                    bg = bg.resize((basewidth, hsize), Image.ANTIALIAS) #Resize bg to 356 px

                    temp.paste(bg, (0, 244), bg) #Place the pfp in the correct spot
                    temp.paste(fg, (0, 0), fg) #Paste the slap on to it

                    temp.save("data/images/cockschelle.png") #Temp image
                    await self.bot.send_file(self.bot.get_channel(id=self.od), 'data/images/cockschelle.png') #Send image to cache channel

                elif len(db[self.person.avatar_url]) is not 0: #Image is in cache
                    img = str(db.get(self.person.avatar_url)) #Get URL from cache
                    img = img.strip("['") #Strip some useless stuff
                    img = img.strip("']")
                    msg2 = "*{slapper}* slaps *{slapped}* with their cock.".format(slapper=self.message.author.display_name, slapped=self.person.display_name)
                    em = discord.Embed(color=discord.Color.red(), title=msg2)
                    em.set_image(url=img)
                    await self.bot.send_message(self.message.channel, embed = em)
        else:
            db = fileIO(self.cache, "load")
            if person.avatar_url not in db:
                db[person.avatar_url] = []
                fileIO(self.cache, "save", db)
            if len(db[person.avatar_url]) == 0:
                server = ctx.message.channel
                pic_ext = ['.jpg','.png','.jpeg']
                self.person = person
                self.message = ctx.message
                fg = Image.open("data/images/slap.png")
                temp = Image.open("data/images/temp.png")
                pfp = person.avatar_url
                response = requests.get(pfp)
                bg = Image.open(BytesIO(response.content))
                bg = bg.convert('RGBA')
                basewidth = 356
                wpercent = (basewidth/float(bg.size[0]))
                hsize = int((float(bg.size[1]) * float(wpercent)))
                bg = bg.resize((basewidth, hsize), Image.ANTIALIAS)
                temp.paste(bg, (0, 244), bg)
                temp.paste(fg, (0, 0), fg)
                temp.save("data/images/cockschelle.png")
                await self.bot.send_file(self.bot.get_channel(id=self.od), 'data/images/cockschelle.png')
            elif len(db[self.person.avatar_url]) is not 0:
                img = str(db.get(self.person.avatar_url))
                img = img.strip("['")
                img = img.strip("']")
                msg2 = "*{slapper}* slaps *{slapped}* with their cock.".format(slapper=self.message.author.display_name, slapped=self.person.display_name)
                em = discord.Embed(color=discord.Color.red(), title=msg2)
                em.set_image(url=img)
                await self.bot.send_message(self.message.channel, embed = em)

    async def on_message(self, mes):
        db = fileIO(self.cache, "load")
        if mes.channel.id == self.od: #Check if the new message is in the cache channel
            if mes.author.id == self.bot.user.id: #Check if it was sent by the bot
                img = mes.attachments[0]['url'] #Pull the URL from it
                db[self.person.avatar_url].append(img) #Add the URL to the cache
                fileIO(self.cache, "save", db) #Save the cache JSON
                msg2 = "*{slapper}* slaps *{slapped}* with their cock.".format(slapper=self.message.author.display_name, slapped=self.person.display_name)
                em = discord.Embed(color=discord.Color.green(), title=msg2)
                em.set_image(url=img)
                await self.bot.send_message(self.message.channel, embed = em)
            else:
                pass
        else:
            pass