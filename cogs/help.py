import discord
import discord.ext.commands as cmd
import asyncio
import random

class GenHelpCommand(cmd.DefaultHelpCommand):
    def get_command_signature(self, command):
        if command.aliases:
            name = f"({command.name} / {' / '.join(command.aliases)})"
        else:
            name = command.name
        return '{0.clean_prefix}{1} {2.signature}'.format(self, name, command)

    async def send_command_help(self, command):
        ctx = self.context
        show = True
        if ctx.author.id != ctx.bot.dev:
            if command.hidden:
                show = False
            else:
                try:
                    await command.can_run(ctx)
                except cmd.NotOwner:
                    show = False
            
        if show:
            color = discord.Colour.from_hsv(random.random(), 1, 1)
            title = self.get_command_signature(command)
            desc = command.help if command.help is not None else " "
            parent = command.full_parent_name
            author = f"Subcommand of '{parent}'" if parent else " "
            cog = f"Category: {command.cog.qualified_name}" if command.cog else "Uncategorized"
            e = discord.Embed(color=color, title=title, description=desc)
            e.set_author(name=author)
            e.set_footer(text=cog)
            await ctx.send(embed=e)
        else:
            await ctx.send("Sorry pal, you can't see this~")
        
        
        
class Help(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nsfw = False
        self._original_help_command = bot.help_command
        bot.help_command = GenHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Help(bot))