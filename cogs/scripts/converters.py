import discord
from discord.ext import commands

class CustomUser(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            member = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                member = await commands.UserConverter().convert(ctx, argument)
            except commands.BadArgument:
                try:
                    member = await ctx.bot.fetch_user(int(argument))
                except Exception as e:
                    if isinstance(e, TypeError):
                        raise BadArgument("The name/name#discrim/ID/mention lookup failed.")
        if member:
            return member
        raise BadArgument("The name/name#discrim/ID/mention lookup failed.")