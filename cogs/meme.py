import discord
import os
import os.path
import random
from .utils import checks
from .utils.dataIO import dataIO
from discord.ext import commands

class Meme:
    """Want sum shitpost."""

    @commands.command(pass_context=False)
    async def cursed(self):
        """Upload a file from your local folder"""

        state = random.getstate()
        num = random.randint(1, 55)
        random.setstate(state)
        await self.bot.upload(fp = data/meme/{}.jpg).format(num)

        
        
def check_folders():
    folders = ('data', 'data/meme')
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)

def setup(bot):
    check_folders()
    bot.add_cog(Meme(bot))