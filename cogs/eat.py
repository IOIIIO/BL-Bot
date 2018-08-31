from discord.ext import commands


class eat:
    """Remind the chat how dead it is"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=False, name='eat')
    async def _eat(self, context, *, victim : str=None):
        """Randomly chooses a way to eat."""
        server = context.message.server
        author = context.message.author
        if victim is not None:
            if "<@!" in victim or "<@" in victim:
                if "<@!" in victim:
                    user = victim.replace('<@!', '').replace('>', '')
                if "<@" in victim:
                    user = victim.replace('<@', '').replace('>', '')
                person = self.bot.get_user_info(user)
                if user == author.id:
                    message = str(random.choice(self.eat_self))
                elif user == self.bot.user.id:
                    message = str(random.choice(self.eat_bot))
                elif user != author.id and user != self.bot.user.id:
                    message = str(random.choice(self.eat_person)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
            elif "@everyone" in victim or "@here" in victim:
                await self.bot.say("Nice try funny guy")
            else:
                message = str(random.choice(self.eat_thing)).format(victim=victim)
                await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)
        else:
            message = str(random.choice(self.eat_nothing))
            await self.bot.say(italics(context.message.author.display_name)+ ', ' + message)


def setup(bot):
    bot.add_cog(eat(bot))