import discord, psutil, asyncio
from datetime import datetime
from discord.ext import commands
import time

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def uptime(self, ctx):
    uptime = datetime.utcnow() - self.bot.launch_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    timestamp = int(self.bot.launch_time.timestamp())
    await ctx.reply(
      embed=discord.Embed(
        title="Current Uptime",
        description=f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s\n\nStartup Time: <t:{timestamp}:F>",
        color=0x88FF44
        ),
      delete_after=60
    )

  @commands.command()
  async def invite(self, ctx):
    await ctx.reply(embed=discord.Embed(
        title="Invite me using these links!",
        description=f"[Normal Permissions]({discord.utils.oauth_url(self.bot.user.id, discord.Permissions(274945363009), scopes=('bot', 'applications.commands'))})\n[Moderation Permissions]({discord.utils.oauth_url(self.bot.user.id, discord.Permissions(274945363015), scopes=('bot', 'applications.commands'))}) (Enables Moderation commands)\n",
        color=0x28e8ed
        ),
        delete_after=45
      )

  @commands.command()
  async def quote(self, ctx, message=None):
    if not ctx.message.reference:
      return await ctx.reply("You must use this command while replying to a message.")

    message = ctx.message.reference.resolved
    await ctx.reply(embed=discord.Embed(
      title=f"{message.author} sent:",
      description=f"> {message.content}\n- {message.author.mention}"
      ))

  @commands.command()
  async def ping(self, ctx):
    # connection = self.bot.db
    websocket = self.bot.latency * 1000
    startwrite = time.perf_counter()
    msg = await ctx.reply("Pong!", mention_author=False, delete_after=120)
    endwrite = time.perf_counter()
    # await connection.execute("SELECT 1")
    # start = time.perf_counter()
    # await connection.execute("SELECT 1")
    # end = time.perf_counter()
    # dbping = end - start
    duration = (endwrite - startwrite) * 1000
    await msg.edit(embed=discord.Embed(
      title="Pong!",
      description=f"<a:typing:597589448607399949> Typing\n`{duration:.2f}`ms\n<a:loading:747680523459231834> Websocket\n`{websocket:.2f}`ms",
      color=0x101c6b
      ))

  @commands.command()
  async def battery(self, ctx):
    battery = psutil.sensors_battery()
    await ctx.reply(embed=discord.Embed(
      title="I am alive",
      description=f"{battery.percent}%\n{'Plugged In' if battery.power_plugged else 'Not Plugged In'}", 
      color=0x88FF44 if battery.power_plugged else 0xFF2E2E
      ),
      delete_after=20
    )

  @commands.command()
  async def counter(self, ctx):
    counter = self.bot.command_counter
    await ctx.reply(embed=discord.Embed(
      title="Command Counter",
      description=f"Commands used since last restart: {counter}",
      color=0x1f84c5
      ),
      delete_after=40
    )

  @commands.command(aliases=["about"])
  async def credits(self, ctx):
    version = discord.__version__
    await ctx.reply(embed=discord.Embed(
      title="About me",
      description=f"Hi, my name is Alone Bot.\n My discord.py version is {version}. <:dpy:596577034537402378>\nMy Python version is 3.9.0 <:python:596577462335307777>",
      color=0xcfe2ee
      ),
      delete_after=90
      )
  
  @commands.command(aliases=["ui", "user_info", "user info"])
  async def userinfo(self, ctx, *, member: discord.Member = None):
    if not member:
      member = ctx.author
    jointime = int(member.joined_at.timestamp())
    createdtime = int(member.created_at.timestamp())
    status = member.status
    embed=discord.Embed(title="Userinfo", description=f"Name: {member.name}\nNickname: {member.nick}\nJoined at: <t:{jointime}:F>\nreated at: <t:{createdtime}:F>\nAvatar: [Click Here]({member.avatar_url})\nStatus: {status}\nBanner is currently disabled", color=0x53bdce)
    embed.set_thumbnail(url=member.avatar_url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed, delete_after=240)

  @commands.command(aliases=["server_info", "server info", "si"])
  @commands.guild_only()
  async def serverinfo(self, ctx, guild: discord.Guild = None):
    if not guild:
      guild = ctx.guild
    bots = sum(m.bot for m in guild.members)
    embed = discord.Embed(title="Server Info", description=f"Owner: {guild.owner}\nID: {guild.id}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: Level {guild.premium_tier}", color=0x184ef3)
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed, delete_after=240)

  @commands.command()
  async def support(self, ctx):
    await ctx.reply(embed=discord.Embed(
        title="Support",
        description=f"Join my [support server]({self.bot.support_server})!"
        ),
      delete_after=75
    )

  @commands.command()
  async def suggest(self, ctx, *, arg: str):
    channel = self.bot.get_channel(868117548087005224) or await self.bot.fetch_channel(868117548087005224)
    await channel.send(embed=discord.Embed(title=f"Suggestion by {ctx.author.name}", description=f"`{arg}`", color=0xFFFFFF))
    await ctx.message.add_reaction("\U00002705")
    await ctx.reply("Suggestion sent.")

  @commands.command()
  async def cleanup(self, ctx, limit: int = 50):
    history = await ctx.channel.history(limit=limit).flatten()
    for message in history:
      if message.author == ctx.me:
        await message.delete()
    await ctx.message.add_reaction("\U00002705")

  @commands.command()
  async def afk(self, ctx, *, reason: str = None):
    if self.bot.afk.get(id):
      return await ctx.reply("You are already afk!", delete_after=90)

    await ctx.message.add_reaction("\U00002705")
    await ctx.reply(f"**AFK**\nYou are now afk for {reason}.", delete_after=10)
    self.bot.afk[ctx.author.id] = reason

def setup(bot):
  bot.add_cog(Utility(bot))
