import asyncio
import discord
import discord.ext.commands as cmd

class Admin(cmd.Cog):
    """Commands for settings and/or admin only actions."""
    def __init__(self, bot):
        self.bot = bot
        self.nsfw = False
        
    @cmd.command(name="hackban", aliases=['hb'])
    @cmd.guild_only()
    def _hackban(self, ctx, id):
        """Useful for banning people not on the currect guild."""
        await ctx.guild.ban(discord.Object(id=id))
        
    @_hackban.error
    async def hb_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send("I don't have proper permissions for this :(")
        elif isinstance(error, discord.HTTPExpection):
            await ctx.send("Something went wrong! Do you have the correct ID?")
        else:
            raise error
            
def setup(bot):
    bot.add_cog(Admin(bot))