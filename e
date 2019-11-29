[33mcommit 25f4472efc8bfca5fe82fe84a3a7edcd8a1191ff[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m)[m
Author: Hell Bell <herreracortes03@gmail.com>
Date:   Wed Nov 27 23:36:45 2019 -0300

    information update fix

[1mdiff --git a/bot.py b/bot.py[m
[1mindex 86aea8f..652273e 100644[m
[1m--- a/bot.py[m
[1m+++ b/bot.py[m
[36m@@ -3,6 +3,7 @@[m [mimport asyncio[m
 import aiohttp[m
 import discord.ext.commands as cmd[m
 import os, sys, time[m
[32m+[m[32mimport traceback as tb[m
 import json[m
 [m
 with open(os.path.join(sys.path[0], "config.json"), "r") as config:[m
[1mdiff --git a/cogs/info.py b/cogs/info.py[m
[1mindex 0b93344..4656deb 100644[m
[1m--- a/cogs/info.py[m
[1m+++ b/cogs/info.py[m
[36m@@ -17,11 +17,11 @@[m [mclass Information(cmd.Cog):[m
     async def _user(self, ctx):[m
         """Retrieves several info pieces from user."""[m
         if ctx.invoked_subcommand is None:[m
[31m-            await ctx.send(f"Please do {ctx.prefix} help user for correct usage.")[m
[32m+[m[32m            await ctx.send(f"Please do {ctx.prefix}help user for correct usage.")[m
             [m
[31m-    @cmd.command(aliases=["sinfo"])[m
[32m+[m[32m    @cmd.command(name="servinfo", aliases=["sinfo"])[m
     @cmd.guild_only()[m
[31m-    async def servinfo(self, ctx):[m
[32m+[m[32m    async def _servinfo(self, ctx):[m
         """Displays info about the server."""[m
         g = ctx.guild[m
         if g.mfa_level:[m
[36m@@ -29,7 +29,7 @@[m [mclass Information(cmd.Cog):[m
         else:[m
             a = ":x:"[m
         members = [x for x in g.members if not x.bot][m
[31m-        bots = g.members - members[m
[32m+[m[32m        bots = list(set(g.members) - set(members))[m
         e = discord.Embed(title="SERVER INFO", color=discord.Colour.from_hsv(random.random(), 1, 1))[m
         e.set_thumbnail(url=g.icon_url)[m
         e.add_field(name="Name", value=g.name)[m
[36m@@ -37,66 +37,70 @@[m [mclass Information(cmd.Cog):[m
         e.add_field(name="Created at", value=g.created_at.replace(microsecond=0), inline=False)[m
         e.add_field(name="Members", value=len(members))[m
         e.add_field(name="Bots", value=len(bots))[m
[31m-        e.add_field(name="Channels", value=len(g.channels)[m
[32m+[m[32m        e.add_field(name="Channels", value=len(g.channels))[m
         e.add_field(name="Emotes", value=len(g.emojis), inline=False)[m
         e.add_field(name="2FA administration?", value=a, inline=False)[m
         e.add_field(name="Nitro Boost Tier", value=g.premium_tier)[m
         await ctx.send(embed=e)[m
 [m
     @cmd.command(name="about")[m
[31m-    async def bot_info(self, ctx):[m
[32m+[m[32m    async def _about(self, ctx):[m
         """Displays info about me~"""[m
         color = ctx.me.color if ctx.guild else discord.Colour.from_hsv(random.random(), 1, 1)[m
         e = discord.Embed(title=str(self.bot.user), color=color)[m
         e.set_thumbnail(url=self.bot.user.avatar_url)[m
         nick = "None" if not ctx.me.nick else ctx.me.nick[m
         e.add_field(name="Nickname", value=nick)[m
[31m-        e.add_field(name="ID", value=ctx.bot.id)[m
[31m-        e.add_field(name="Created at", value=self.bot.user.created_at.replace(microsecond=0))[m
[32m+[m[32m        e.add_field(name="ID", value=ctx.bot.user.id)[m
[32m+[m[32m        e.add_field(name="Created at", value=self.bot.user.created_at.replace(microsecond=0), inline=False)[m
         e.add_field(name="Servers", value=len(self.bot.guilds))[m
         e.add_field(name="Members", value=len(self.bot.users))[m
         e.add_field(name="Emotes available", value=len(self.bot.emojis))[m
[32m+[m[32m        e.add_field(name="GitHub repo", value=self.bot.url, inline=False)[m
         await ctx.send(embed=e)[m
 [m
[31m-    @user.command(name="info")[m
[32m+[m[32m    @_user.command(name="info")[m
     async def user_info(self, ctx, *, author: converters.CustomUser = None):[m
         """Sends general info about the author, or a selected user/ID."""[m
[31m-        if author is None:[m
[31m-            author = ctx.author[m
[32m+[m[32m        author = ctx.author if not author else author[m
         avatar = author.avatar_url[m
[31m-        if avatar == None:[m
[31m-            avatar = author.default_avatar_url[m
[32m+[m[32m        avatar = author.default_avatar_url if not avatar else avatar[m
         if isinstance(author, discord.Member):[m
             nick = author.display_name[m
             join = author.joined_at.replace(microsecond=0)[m
             r = "Member (in this server)"[m
             color = author.colour[m
[32m+[m[32m            tr = f"{author.top_role} ({author.top_role.id})"[m
[32m+[m[32m            if author == ctx.guild.owner:[m
[32m+[m[32m                adm = "Yes, owner"[m
[32m+[m[32m            elif author.guild_permissions.administrator:[m
[32m+[m[32m                adm = "Yes"[m
[32m+[m[32m            else:[m
[32m+[m[32m                adm = "No"[m
         else:[m
             nick = "**-**"[m
             join = "**-**"[m
             r = "User (not in this server)"[m
             color = discord.Colour.from_hsv(random.random(), 1, 1)[m
[31m-        if author.premium:[m
[31m-            if author.premium_type is discord.PremiumType.classic:[m
[31m-                prem = "Yes, Classic"[m
[31m-            else:[m
[31m-                prem = "Yes"[m
[31m-        else:[m
[31m-            prem = "No"[m
[32m+[m[32m            tr = "**-**"[m
[32m+[m[32m            adm = "**-**"[m
[32m+[m[32m        isbot = "Yes" if author.bot else "No"[m
         e = discord.Embed(title="User Info", color=color)[m
         e.set_thumbnail(url=avatar)[m
         e.add_field(name="User#Disc", value=author)[m
         e.add_field(name="ID", value=author.id)[m
[31m-        e.add_field(name="Nickname", value=nick)[m
[31m-        e.add_field(name="Created at", value=author.created_at.replace(microsecond=0))[m
[32m+[m[32m        e.add_field(name="Nickname", value=nick, inline=False)[m
[32m+[m[32m        e.add_field(name="Bot?", value=isbot)[m
[32m+[m[32m        e.add_field(name="Created at", value=author.created_at.replace(microsecond=0), inline=False)[m
         e.add_field(name="Joined at", value=join)[m
         e.add_field(name="User or Member?", value=r, inline=False)[m
[31m-        e.add_field(name="Nitro user?", value=prem, inline=False)[m
[31m-        e.add_field(name="Avatar URL", value=str(avatar))[m
[32m+[m[32m        e.add_field(name="Top role", value=tr)[m
[32m+[m[32m        e.add_field(name="Admin?", value=adm)[m
[32m+[m[32m        e.add_field(name="Avatar URL", value=str(avatar), inline=False)[m
         await ctx.send(embed=e)[m
 [m
[31m-    @user.command(aliases=["pfp", "pic"])[m
[31m-    async def avatar(self, ctx, *, msg: converters.CustomUser = None):[m
[32m+[m[32m    @_user.command(name="avatar", aliases=["pfp", "pic"])[m
[32m+[m[32m    async def _avatar(self, ctx, *, msg: converters.CustomUser = None):[m
         """Messages a member's (or the author's) avatar back."""[m
         if msg is None:[m
             async with self.session.get(str(ctx.author.avatar_url)) as resp:[m
[36m@@ -109,7 +113,7 @@[m [mclass Information(cmd.Cog):[m
                 avatar = discord.File(fp=buffer, filename='avatar.webp')[m
                 await ctx.send(content=f'{msg.display_name}\'s avatar:', file=avatar)[m
      [m
[31m-    @avatar.error[m
[32m+[m[32m    @_avatar.error[m
     async def avatar_error(self, ctx, error):[m
         if isinstance(error, cmd.BadArgument) or isinstance(error, cmd.MissingRequiredArgument):[m
             await ctx.send("Input a valid ID, or mention a member (only one!).")[m
[1mdiff --git a/cogs/scripts/converters.py b/cogs/scripts/converters.py[m
[1mnew file mode 100644[m
[1mindex 0000000..8acc48e[m
[1m--- /dev/null[m
[1m+++ b/cogs/scripts/converters.py[m
[36m@@ -0,0 +1,19 @@[m
[32m+[m[32mimport discord[m
[32m+[m[32mfrom disc