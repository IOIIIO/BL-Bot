import discord, os, random
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


def setup(bot):
    bot.add_cog(Clippy(bot))

class Clippy:

    def __init__(self, bot):
        self.bot = bot

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
    
    @commands.command(pass_context=True)
    async def clippy(self, ctx, *,text: str = ""):
        """I *know* you wanted some help with something - what was it?"""
        image = Image.open('data/images/clippy.png')
        image_size = image.size
        image_height = image.size[1]
        image_width = image.size[0]
        draw = ImageDraw.Draw(image)
        server = ctx.message.channel

        text = text
        # Remove any non-ascii chars
        text = ''.join([i for i in text if ord(i) < 128])

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

        font = ImageFont.truetype('data/images/comic.ttf', size=20)
        #340 is the width we want to set the image width to
        lines = self.text_wrap(text, font, 340)
        line_height = font.getsize('hg')[1]
        (x, y) = (25, 20)
        color = 'rgb(0, 0, 0)' # black color
        text_size = draw.textsize(text, font=font)

        for line in lines:
            text_size = draw.textsize(line, font=font)
            image_x = (image_width /2 ) - (text_size[0]/2)
            draw.text((image_x, y), line, fill=color, font=font)
            y = y + line_height

        image.save('data/images/clippynow.png')
        await self.bot.send_file(server, 'data/images/clippynow.png')

        # Remove the png
        os.remove("data/images/clippynow.png")

    @commands.command(pass_context=True)
    async def hilda(self, ctx, *,text: str = ""):
        """Is this a meme?"""
        image = Image.open('data/images/hilda.png')
        image_size = image.size
        image_height = image.size[1]
        image_width = image.size[0]
        draw = ImageDraw.Draw(image)
        server = ctx.message.channel

        text = text
        # Remove any non-ascii chars
        text = ''.join([i for i in text if ord(i) < 128])

        clippy_errors = [
            "I guess I couldn't print that... whatever it was.",
            "It looks like you're trying to break things!  Maybe I can help.",
            "Whoops, I guess I wasn't coded to understand that.",
            "After filtering your input, I've come up with... well... nothing.",
            "Nope.",
            "y u du dis to Hilda :("
        ]

        if not len(text):
            text = random.choice(clippy_errors)

        font = ImageFont.truetype('data/images/comic.ttf', size=40)
        #340 is the width we want to set the image width to
        lines = self.text_wrap(text, font, 450)
        line_height = font.getsize('hg')[1]
        (x, y) = (477, 120)
        color = 'rgb(0, 0, 0)' # black color
        text_size = draw.textsize(text, font=font)

        for line in lines:
            text_size = draw.textsize(line, font=font)
            #image_x = (image_width /2 ) - (text_size[0]/2)
            image_x = 460 - (text_size[0]/2)
            draw.text((image_x, y), line, fill=color, font=font)
            y = y + line_height 

        image.save('data/images/hildanow.png')
        await self.bot.send_file(server, 'data/images/hildanow.png')

        # Remove the png
        os.remove("data/images/hildanow.png")