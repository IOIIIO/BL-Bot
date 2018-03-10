import os
import random
import discord
from .utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class Kill:
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'data/kill/kill.json'
        self.kills = dataIO.load_json(self.filename)
        self.ways_to_kill = []
        self.ways_to_kill.append('{killer} shoves a double barreled shotgun into {victim}\'s mouth and squeezes the trigger of the gun, causing {victim}\'s head to horrifically explode like a ripe pimple, splattering the young person\'s brain matter, gore, and bone fragments all over the walls and painting it a crimson red.')
        self.ways_to_kill.append('Screaming in sheer terror and agony, {victim} is horrifically dragged into the darkness by unseen forces, leaving nothing but bloody fingernails and a trail of scratch marks in the ground from which the young person had attempted to halt the dragging process.')
        self.ways_to_kill.append('{killer} takes a machette and starts hacking away on {victim}, chopping {victim} into dozens of pieces.')
        self.ways_to_kill.append('{killer} pours acid over {victim}. *"Well don\'t you look pretty right now?"*')
        self.ways_to_kill.append('{victim} screams in terror as a giant creature with huge muscular arms grab {victim}\'s head; {victim}\'s screams of terror are cut off as the creature tears off the head with a sickening crunching sound. {victim}\'s spinal cord, which is still attached to the dismembered head, is used by the creature as a makeshift sword to slice a perfect asymmetrical line down {victim}\'s body, causing the organs to spill out as the two halves fall to their) respective sides.')
        self.ways_to_kill.append('{killer} grabs {victim}\'s head and tears it off with superhuman speed and efficiency. Using {victim}\'s head as a makeshift basketball, {killer} expertly slams dunk it into the basketball hoop, much to the applause of the audience watching the gruesome scene.')
        self.ways_to_kill.append('{killer} uses a shiv to horrifically stab {victim} multiple times in the chest and throat, causing {victim} to gurgle up blood as the young person horrifically dies.')
        self.ways_to_kill.append('{victim} screams as {killer} lifts {victim} up using his superhuman strength. Before {victim} can even utter a scream of terror, {killer} uses his superhuman strength to horrifically tear {victim} into two halves; {victim} stares at the monstrosity in shock and disbelief as {victim} gurgles up blood, the upper body organs spilling out of the dismembered torso, before the eyes roll backward into the skull.')
        self.ways_to_kill.append('{victim} steps on a land mine and is horrifically blown to multiple pieces as the device explodes, the {victim}\'s entrails and gore flying up and splattering all around as if someone had thrown a watermelon onto the ground from the top of a multiple story building.')
        self.ways_to_kill.append('{victim} is killed instantly as the top half of his head is blown off by a Red Army sniper armed with a Mosin Nagant, {victim}\'s brains splattering everywhere in a horrific fashion.')

    async def save_kills(self):
        dataIO.save_json(self.filename, self.kills)

    @commands.command(pass_context=True, no_pm=True, name='kill')
    async def _kill(self, context, victim: discord.Member):
        """Randomly chooses a kill."""
        server = context.message.server
        author = context.message.author
        if victim.id == author.id:
            message = 'I won\'t let you kill yourself!'
        elif victim.id == self.bot.user.id:
            message = 'I refuse to kill myself!'
        else:
            if server.id in self.kills:
                x = list(self.kills[server.id].keys())
                message = self.kills[server.id][random.choice(x)]['text'].format(victim=victim.display_name, killer=author.display_name)
            else:
                message = str(random.choice(self.ways_to_kill)).format(victim=victim.display_name, killer=author.display_name)
        await self.bot.say(message)

    @commands.command(pass_context=True, name='removekill')
    @checks.mod_or_permissions(administrator=True)
    async def _removekill(self, context, name):
        """Remove a kill"""
        server = context.message.server
        if server.id not in self.kills or name.lower() not in self.kills[server.id]:
            message = 'I do not know `{}`'.format(name)
        else:
            del self.kills[server.id][name.lower()]
            await self.save_kills()
            message = 'Kill removed.'
        await self.bot.say(message)

    @commands.command(pass_context=True, name='addkill')
    @checks.mod_or_permissions(administrator=True)
    async def _addkill(self, context, name, *kill_text):
        """Variables:
        {killer} adds the name of the killer
        {victim} adds the name of the victim
        """
        server = context.message.server
        if server.id not in self.kills:
            self.kills[server.id] = {}
        if name.lower() not in self.kills[server.id]:
            try:
                int(name)
            except:
                self.kills[server.id][name.lower()] = {}
                self.kills[server.id][name.lower()]['text'] = ' '.join(kill_text)
                await self.save_kills()
                message = 'Kill added.'
            else:
                message = 'Name cannot be a number alone, it must contain characters.'
        else:
            message = 'This kill is already in here! perform `{}removekill <name>` to remove it.'.format(context.prefix)
        await self.bot.say(message)


def check_folder():
    if not os.path.exists('data/kill'):
        print('Creating data/kill folder...')
        os.makedirs('data/kill')


def check_file():
    data = {}
    f = 'data/kill/kill.json'
    if not dataIO.is_valid_json(f):
        print('Creating default kill.json...')
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    n = Kill(bot)
    bot.add_cog(n)