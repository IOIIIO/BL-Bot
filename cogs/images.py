import discord, os, random
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


def setup(bot):
    bot.add_cog(Clippy(bot))

class Clippy:

    def __init__(self, bot):
        self.bot = bot
        #self.height = 0

    def text_wrap(self, text, font, max_width):
        # Replace \n, \r, and \t with a space
        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        # Let's ensure the text is only single-spaced
        text = " ".join([x for x in text.split(" ") if len(x)])
        lines = []
        # If the width of the text is smaller than image width
        # we don't need to split it, just add it to the lines array
        # and return
        if font.getsize(text)[0] <= max_width:
            lines.append(text)
        else:
            # split the line by spaces to get words
            words = text.split(' ')
            i = 0
            # append every word to a line while its width is shorter than image width
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                # when the line gets longer than the max width do not append the word,
                # add the line to the lines array
                lines.append(line)
        return lines

    async def imagehilda(self, xc, yc, size, text, ix, ln, tp):
        if tp == 1:
            image = Image.open('data/images/hilda.png')
        else:
            image = Image.open('data/images/clippy.png')
        image_size = image.size
        image_height = image.size[1]
        image_width = image.size[0]
        if tp == 0:
            ix = (image_width/2)
        draw = ImageDraw.Draw(image)
        
        font = ImageFont.truetype('data/images/comic.ttf', size=size)
        lines = self.text_wrap(text, font, ln)
        line_height = font.getsize('hg')[1]
        (x, y) = (xc, yc)
        color = 'rgb(0, 0, 0)' # black color
        text_size = draw.textsize(text, font=font)

        for line in lines:
            text_size = draw.textsize(line, font=font)
            #image_x = (image_width /2 ) - (text_size[0]/2)
            image_x = ix - (text_size[0]/2)
            draw.text((image_x, y), line, fill=color, font=font)
            y = y + line_height
            self.height = y

        self.image = image 
    
    @commands.command(pass_context=True)
    async def clippy(self, ctx, *,text: str = ""):
        """I *know* you wanted some help with something - what was it?"""

        server = ctx.message.channel
        clippy_errors = [
            "I guess I couldn't print that... whatever it was.",
            "It looks like you're trying to break things!  Maybe I can help.",
            "Whoops, I guess I wasn't coded to understand that.",
            "After filtering your input, I've come up with... well... nothing.",
            "Nope.",
            "y u du dis to clippy :("
        ]

        if not len(text):
            text = random.choice(clippy_errors)

        await self.imagehilda(25, 20, 20, text, 84, 340, 0)
        if self.height > 181:
            s = 20
            while self.height > 181 and s > 9:
                s = s-2
                if s < 11:
                    await self.bot.say("I'm sorry, that message is too long.")
                    abort = 1
                    break    
                else:
                    await self.imagehilda(25, 20, s, text, s, 340, 0)
                    abort = 0
            if abort == 0:
                self.image.save('data/images/clippynow.png')
                await self.bot.send_file(server, 'data/images/clippynow.png')
                # Remove the png
                try:
                    os.remove("data/images/clippynow.png")   
                except:
                    return
        else:
            self.image.save('data/images/clippynow.png')
            await self.bot.send_file(server, 'data/images/clippynow.png')
            # Remove the png
            try:
                os.remove("data/images/clippynow.png")
            except:
                    return

    @commands.command(aliases=["Hilda"], pass_context=True)
    async def hilda(self, ctx, *,text: str = ""):
        """Is this a meme?"""
        
        abort = 0
        server = ctx.message.channel
        hilda_errors = [
            "I guess I couldn't print that... whatever it was.",
            "It looks like you're trying to break things!  Maybe I can help.",
            "Whoops, I guess I wasn't coded to understand that.",
            "After filtering your input, I've come up with... well... nothing.",
            "Nope.",
            "y u du dis to Hilda :("
        ]

        if not len(text):
            text = random.choice(hilda_errors)


        await self.imagehilda(477, 120, 40, text, 460, 450, 1)
        if self.height > 353:
            s = 40
            while self.height > 353 and s > 18:
                s = s-2
                if s < 20:
                    await self.bot.say("I'm sorry, that message is too long.")
                    abort = 1
                    break    
                else:
                    await self.imagehilda(477, 120, s, text, 460, 450, 1)
                    abort = 0
            if abort == 0:
                self.image.save('data/images/hildanow.png')
                await self.bot.send_file(server, 'data/images/hildanow.png')
                # Remove the png
                try:
                    os.remove("data/images/hildanow.png")
                except:
                    return           
        else:
            self.image.save('data/images/hildanow.png')
            await self.bot.send_file(server, 'data/images/hildanow.png')
            # Remove the png
            try:
                os.remove("data/images/hildanow.png")
            except:
                    return