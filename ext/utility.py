from __future__ import annotations

import discord, psutil, asyncio
from datetime import datetime
from discord.ext import commands
import time

class Utility(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx: commands.Context) -> None:
        uptime = discord.utils.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        timestamp = int(self.bot.launch_time.timestamp())
        await ctx.reply(
            embed=self.bot.generate_embed(ctx, "Current Uptime", f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s\n\nStartup Time: <t:{timestamp}:F>", "88FF44"),
            mention_author=False,
            delete_after=60
        )

    @commands.command()
    async def invite(self, ctx: commands.Context) -> None:
        await ctx.reply(
            embed=self.bot.generate_embed(ctx, "Invite me using this link!", f"[Normal Permissions](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=274945363009&scope=applications.commands%20bot)\n\n[Moderation Permissions](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=274945363015&scope=applications.commands%20bot) (Enables Moderation commands)\n", "28e8ed"),
            mention_author=False,
            delete_after=45
        )

    @commands.command()
    async def quote(self, ctx: commands.Context, message=None):
        if not message:
            message = ctx.message.reference.resolved
        await ctx.reply(
            embed=self.bot.generate_embed(ctx, f"{message.author} sent:", f"> {message.content}\n- {message.author.mention}"),
            mention_author=False
        )

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        websocket = self.bot.latency * 1000
        startwrite = time.perf_counter()
        msg = await ctx.reply("Pong!", mention_author=False, delete_after=120)
        endwrite = time.perf_counter()

        duration = (endwrite - startwrite) * 1000
        await msg.edit(embed=self.bot.generate_embed(ctx, "Pong!", f"<a:typing:597589448607399949> Typing\n`{duration:.2f}`ms\n<a:loading:747680523459231834> Websocket\n`{websocket:.2f}`ms", "101c6b"), mention_author=False)

    @commands.command()
    async def battery(self, ctx: commands.Context) -> None:
        battery = psutil.sensors_battery()
        await ctx.reply(embed=self.bot.generate_embed(ctx, "I am alive", f"{battery.percent}%\n{'Plugged In' if battery.power_plugged else 'Not Plugged In'}", f"{'88FF44' if battery.power_plugged else 'FF2E2E'}"), mention_author=False, delete_after=20)

    @commands.command()
    async def counter(self, ctx: commands.Context) -> None:
        counter = self.bot.command_counter
        await ctx.reply(embed=self.bot.generate_embed(ctx, "Command Counter", f"Commands used since last restart: {counter}", "1f84c5"), mention_author=False, delete_after=40)

    @commands.command(aliases=["about"])
    async def credits(self, ctx: commands.Context) -> None:
        version = discord.__version__
        await ctx.reply(embed=self.bot.generate_embed(ctx, "About me",f"Hi, my name is Alone Bot.\n My discord.py version is {version}. <:dpy:596577034537402378>\nMy Python version is 3.9.0 <:python:596577462335307777>", "cfe2ee"), mention_author=False, delete_after=90)
    
    @commands.command(aliases=["ui", "user_info", "user info"])
    async def userinfo(self, ctx: commands.Context, *, member: discord.Member = None):
        if not member:
          member = ctx.author
        jointime = int(member.joined_at.timestamp())
        createdtime = int(member.created_at.timestamp())
        status = member.status
        uiembed=discord.Embed(title="Userinfo", description=f"Name: {member.name}\nNickname: {member.nick}\nJoined at: <t:{jointime}:F>\nreated at: <t:{createdtime}:F>\nAvatar: [Click Here]({member.avatar_url})\nStatus: {status}\nBanner is currently disabled", color=0x53bdce)
        uiembed.set_thumbnail(url=member.avatar_url)
        uiembed.timestamp = datetime.utcnow()
        uiembed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=uiembed, mention_author=False, delete_after=240)

    @commands.command(aliases=["server_info", "server info", "si"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context, guild: discord.Guild = None):
        if not guild:
            guild = ctx.guild
        members = len([members for members in guild.members])
        bots = sum(m.bot for m in guild.members)
        siembed = discord.Embed(title="Server Info", description=f"Owner: {guild.owner}\nID: {guild.id}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: Level {guild.premium_tier}", color=0x184ef3)
        siembed.set_thumbnail(url=guild.icon_url)
        siembed.timestamp = datetime.utcnow()
        siembed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=siembed, mention_author=False, delete_after=240)

    @commands.command()
    async def support(self, ctx: commands.Context) -> None:
        await ctx.reply(embed=self.bot.generate_embed(ctx, "Support", f"Join my [support server]({self.bot.support_server})!"), mention_author=False, delete_after=75)

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, arg: str):
        channel = await self.bot.fetch_channel(868117548087005224)
        await channel.send(embed=self.bot.generate_embed(ctx, f"Suggestion by {ctx.author.name}", f"`{arg}`", "FFFFFF"))
        await ctx.message.add_reaction("\U00002705")
        await ctx.reply("Suggestion sent.", mention_author=False)

    @commands.command()
    async def cleanup(self, ctx: commands.Context, limit: int = None):
        limit = limit or 50
        history = await ctx.channel.history(limit=limit).flatten()
        for message in history:
            if message.author == ctx.me:
                await message.delete()

        await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: str = None):
        if self.bot.afk.get(id) is not None:
            return await ctx.reply("You are already afk!", mention_author=False, delete_after=90)
        await ctx.message.add_reaction("\U00002705")
        await ctx.reply(f"**AFK**\nYou are now afk for {reason}.", mention_author=False, delete_after=10)
        await asyncio.sleep(2.5)
        self.bot.afk[ctx.author.id] = reason

def setup(bot: commands.AutoShardedBot) -> None:
    bot.add_cog(Utility(bot))
