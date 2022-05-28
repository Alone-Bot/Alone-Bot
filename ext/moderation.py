import discord
from discord.ext import commands

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx):
    if not ctx.guild:
      return False
    return True

  @commands.command()
  @commands.bot_has_guild_permissions(ban_members=True)
  @commands.has_guild_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member = None, *, reason: str = "No reason provided."):
    if member == None:
      return await ctx.reply(embed=discord.Embed(
        title="An error occured",
        description="You need to provide a member to ban."
        ))
    await member.ban(reason=reason)
    await ctx.reply(f"Banned {member} for {reason}.")

  @commands.command()
  @commands.bot_has_guild_permissions(kick_members=True)
  @commands.has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member = None, *, reason: str = "No reason provided."):
    if member == None:
      return await ctx.reply(embed=discord.Embed(
            title="An error occured",
            description="You need to provide a member to kick."
          ))
    await member.kick(reason=reason)
    await ctx.reply(f"Kicked {member} for {reason}.", mention_author=False)

  @commands.command()
  @commands.bot_has_guild_permissions(manage_messages=True)
  @commands.has_guild_permissions(manage_messages=True)
  async def purge(self, ctx, limit: int = 20):
    messages = await ctx.channel.purge(limit=limit)
    await ctx.send(f"{len(messages)} messages deleted.", delete_after=15)

def setup(bot):
  bot.add_cog(Moderation(bot))
