import asyncio
import discord
import discord.ext.commands as cmd
from io import BytesIO
import aiohttp
from cogs.scripts import converters
import random


class Information(cmd.Cog):
    """Commands for retrieving information about users, servers, and the bot."""
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        
    @cmd.group(name="user")
    async def _user(self, ctx):
        """Retrieves several info pieces from user."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Please do {ctx.prefix} help user for correct usage.")
            
    @cmd.command(aliases=["sinfo"])
    @cmd.guild_only()
    async def servinfo(self, ctx):
        """Displays info about the server."""
        g = ctx.guild
        if g.mfa_level:
            a = ":white_check_mark:"
        else:
            a = ":x:"
        members = [x for x in g.members if not x.bot]
        bots = g.members - members
        e = discord.Embed(title="SERVER INFO", color=discord.Colour.from_hsv(random.random(), 1, 1))
        e.set_thumbnail(url=g.icon_url)
        e.add_field(name="Name", value=g.name)
        e.add_field(name="Owner", value=g.owner)
        e.add_field(name="Created at", value=g.created_at.replace(microsecond=0), inline=False)
        e.add_field(name="Members", value=len(members))
        e.add_field(name="Bots", value=len(bots))
        e.add_field(name="Channels", value=len(g.channels)
        e.add_field(name="Emotes", value=len(g.emojis), inline=False)
        e.add_field(name="2FA administration?", value=a, inline=False)
        e.add_field(name="Nitro Boost Tier", value=g.premium_tier)
        await ctx.send(embed=e)

    @cmd.command(name="about")
    async def bot_info(self, ctx):
        """Displays info about me~"""
        color = ctx.me.color if ctx.guild else discord.Colour.from_hsv(random.random(), 1, 1)
        e = discord.Embed(title=str(self.bot.user), color=color)
        e.set_thumbnail(url=self.bot.user.avatar_url)
        nick = "None" if not ctx.me.nick else ctx.me.nick
        e.add_field(name="Nickname", value=nick)
        e.add_field(name="ID", value=ctx.bot.id)
        e.add_field(name="Created at", value=self.bot.user.created_at.replace(microsecond=0))
        e.add_field(name="Servers", value=len(self.bot.guilds))
        e.add_field(name="Members", value=len(self.bot.users))
        e.add_field(name="Emotes available", value=len(self.bot.emojis))
        await ctx.send(embed=e)

    @user.command(name="info")
    async def user_info(self, ctx, *, author: converters.CustomUser = None):
        """Sends general info about the author, or a selected user/ID."""
        if author is None:
            author = ctx.author
        avatar = author.avatar_url
        if avatar == None:
            avatar = author.default_avatar_url
        if isinstance(author, discord.Member):
            nick = author.display_name
            join = author.joined_at.replace(microsecond=0)
            r = "Member (in this server)"
            color = author.colour
        else:
            nick = "**-**"
            join = "**-**"
            r = "User (not in this server)"
            color = discord.Colour.from_hsv(random.random(), 1, 1)
        if author.premium:
            if author.premium_type is discord.PremiumType.classic:
                prem = "Yes, Classic"
            else:
                prem = "Yes"
        else:
            prem = "No"
        e = discord.Embed(title="User Info", color=color)
        e.set_thumbnail(url=avatar)
        e.add_field(name="User#Disc", value=author)
        e.add_field(name="ID", value=author.id)
        e.add_field(name="Nickname", value=nick)
        e.add_field(name="Created at", value=author.created_at.replace(microsecond=0))
        e.add_field(name="Joined at", value=join)
        e.add_field(name="User or Member?", value=r, inline=False)
        e.add_field(name="Nitro user?", value=prem, inline=False)
        e.add_field(name="Avatar URL", value=str(avatar))
        await ctx.send(embed=e)

    @user.command(aliases=["pfp", "pic"])
    async def avatar(self, ctx, *, msg: converters.CustomUser = None):
        """Messages a member's (or the author's) avatar back."""
        if msg is None:
            async with self.session.get(str(ctx.author.avatar_url)) as resp:
                buffer = BytesIO(await resp.read())
                avatar = discord.File(fp=buffer, filename='avatar.webp')
                await ctx.send(content=f'{ctx.author}\'s avatar:', file=avatar)
        else:
            async with self.session.get(str(msg.avatar_url)) as resp:
                buffer = BytesIO(await resp.read())
                avatar = discord.File(fp=buffer, filename='avatar.webp')
                await ctx.send(content=f'{msg.display_name}\'s avatar:', file=avatar)
     
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, cmd.BadArgument) or isinstance(error, cmd.MissingRequiredArgument):
            await ctx.send("Input a valid ID, or mention a member (only one!).")


def setup(bot):
    bot.add_cog(Information(bot))