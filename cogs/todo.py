from discord.ext import commands
from cogs.utils import checks
import datetime
from cogs.utils.dataIO import fileIO
import discord
import asyncio
import os

inv_settings = {"Messages"}

class Todo:
    def __init__(self, bot):
        self.bot = bot
        self.direct = "data/todo/todo.json"

    @commands.group(name='todo', pass_context=True)
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @todo.command(name='list', pass_context=True)
    async def list(self, ctx):
        db = fileIO(self.direct, "load")
        if ctx.discord.Member.id in db:
            //Add code for splitting on comma here.
        else:
            await self.bot.say("No items on your todo list. You can add one using `todo add`")

    @todo.command(name='add', pass_context=True)
    async def add(self, ctx, message : str):
        """Set the channel to send notifications too"""
        server = ctx.message.author
        db = fileIO(self.direct, "load")
        if server.id in db:
            db[server.id]['Messages'].append(message)
            fileIO(self.direct, "save", db)
            await self.bot.say("Message added.")
            return
        if not server.id in db:
            db[server.id] = inv_settings
            db[server.id]["Messages"].append(message)
            fileIO(self.direct, "save", db)
            await self.bot.say("A new todo list has been created and your message added.")
        else:
            return
##############################################
    @modlogset.command(pass_context=True, no_pm=True)
    async def embed(self, ctx):
        """Enables or disables embed modlog."""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["embed"] == False:
            db[server.id]["embed"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Enabled embed modlog.")
        elif db[server.id]["embed"] == True:
            db[server.id]["embed"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Disabled embed modlog.")

    async def on_voice_state_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['togglevoice'] == False:
            return
        if before.bot:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        if db[server.id]["embed"] == True:
            name = before
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            updmessage = discord.Embed(description=name, colour=discord.Color.blue())
            infomessage = "__{}__'s voice status has changed".format(before.name)
            updmessage.add_field(name="Info:", value=infomessage, inline=False)
            updmessage.add_field(name="Voice Channel Before:", value=before.voice_channel)
            updmessage.add_field(name="Voice Channel After:", value=after.voice_channel)
            updmessage.set_footer(text="User ID: {}".format(before.id))
            updmessage.set_author(name=time.strftime(fmt) + " - Voice Channel Changed",
                                  url="http://i.imgur.com/8gD34rt.png")
            updmessage.set_thumbnail(url="http://i.imgur.com/8gD34rt.png")
            try:
                await self.bot.send_message(server.get_channel(channel), embed=updmessage)
            except:
                pass
        else:
            await self.bot.send_message(server.get_channel(channel),
                                        ":person_with_pouting_face::skin-tone-3: `{}` **{}'s** voice status has updated. **Channel**: {}\n**Local Mute:** {} **Local Deaf:** {} **Server Mute:** {} **Server Deaf:** {}".format(
                                            time.strftime(fmt), after.name, after.voice_channel, after.self_mute,
                                            after.self_deaf, after.mute, after.deaf))

def check_folder():
    if not os.path.exists('data/modlogset'):
        print('Creating data/modlogset folder...')
        os.makedirs('data/modlogset')


def check_file():
    f = 'data/modlogset/settings.json'
    if not fileIO(f, 'check'):
        print('Creating default settings.json...')
        fileIO(f, 'save', {})


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Todo(bot))