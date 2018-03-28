import os
from .utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class InVoice:
    """Gives a custom role to anyone who enters a voice channel. THIS ROLE MUST EXIST AND THE BOT MUST HAVE THE RIGHTS TO CHANGE ROLES FOR IT TO WORK!"""
    def __init__(self, bot):
        self.bot = bot
        self.data = dataIO.load_json('data/invoice/settings.json')

    async def _save_data(self):
        dataIO.save_json('data/invoice/settings.json', self.data)

    async def _on_voice_state_update(self, before, after):
        try:
            server = after.server
            if server.id in self.data:
                server_role = self.data[server.id]['ROLE']
                if server_role:
                    for role in server.roles:
                        if role.name.lower() == server_role.lower():
                            if role in after.roles and after.voice_channel is None:
                                await self.bot.remove_roles(after, role)
                            elif role not in before.roles and after.voice_channel:
                                await self.bot.add_roles(after, role)
        except Exception as e:
            print('Houston, we have a problem: {}'.format(e))

    @commands.command(pass_context=True, name='invoicerole')
    @checks.mod_or_permissions(administrator=True)
    async def _invoicerole(self, context, role):
        """Set a role"""
        server = context.message.server
        roles = [r.name.lower() for r in server.roles]
        if role.lower() in roles:
            if server.id not in self.data:
                self.data[server.id] = {}
            self.data[server.id]['ROLE'] = role
            await self._save_data()
            message = 'Role `{}` set for Invoice.'.format(role)
        else:
            message = 'Role `{}` does not exist on this server.'.format(role)
        await self.bot.say(message)


def check_folder():
    if not os.path.exists("data/invoice"):
        print("Creating data/invoice folder...")
        os.makedirs("data/invoice")


def check_file():
    data = {}
    f = "data/invoice/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default settings.json...")
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    n = InVoice(bot)
    bot.add_listener(n._on_voice_state_update, 'on_voice_state_update')
    bot.add_cog(n)