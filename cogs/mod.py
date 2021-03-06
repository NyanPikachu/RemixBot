'''
MIT License

Copyright (c) 2017-2018 Cree-Py

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import discord
from discord.ext import commands
import asyncio


class Mod:
    '''Commands for modeators in a guild.'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason='No reason.'):
        '''Kick a member from the guild'''
        try:
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f"Kicked {user.name} from the server.")
        except discord.Forbidden:
            await ctx.send("I could not kick the user. Make sure I have the kick members permission.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason='No reason.'):
        '''Ban a member from the guild'''
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Banned {user.name} from the server.")
        except discord.Forbidden:
            await ctx.send("I could not ban the user. Make sure I have the ban members permission.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, user: discord.Member, time: int=15):
        '''Mute a member in the guild'''
        try:
            secs = time * 60
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await ctx.channel.set_permissions(user, send_messages=False)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(user, connect=False)
            await ctx.send(f"{user.mention} has been muted for {time} minutes.")
            await asyncio.sleep(secs)
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await ctx.channel.set_permissions(user, send_messages=None)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(user, connect=None)
            await ctx.send(f'{user.mention} has been unmuted from the guild.')
        except discord.Forbidden:
            await ctx.send("I could not mute the user. Make sure I have the manage channels permission.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmute a member in the guild'''
        try:
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await ctx.channel.set_permissions(user, send_messages=None)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(user, connect=None)
            await ctx.send(f'{user.mention} has been unmuted from the guild.')
        except discord.Forbidden:
            await ctx.send("I could not unmute the user. Make sure I have the manage channels permission.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        '''Warn a member via DMs'''
        warning = f"You have been warned in **{ctx.message.guild}** by **{ctx.message.author}** for {reason}"
        if not reason:
            warning = f"You have been warned in **{ctx.message.guild}** by **{ctx.message.author}**"
        await user.send(warning)
        await ctx.send(f"**{user}** has been **warned**")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        '''Delete messages a certain number of messages from a channel.'''
        if messages > 99:
            messages = 99

        try:
            await ctx.channel.purge(limit=messages + 1)
        except Exception as e:
            await ctx.send("I cannot delete the messages. Make sure I have the manage messages permission.")
        else:
            await ctx.send(f'{messages} messages deleted. 👌', delete_after=3)


def setup(bot):
    bot.add_cog(Mod(bot))
