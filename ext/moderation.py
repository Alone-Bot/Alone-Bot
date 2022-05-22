from __future__ import annotations

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            return False
        return True

    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = "No reason provided."):
      if member is None:
          await ctx.reply(
              embed=self.bot.generate_embed("An error occured", "You need to provide a member to ban."),
              mention_author=False
          )
          return

      await member.ban(reason=reason)
      await ctx.reply(f"Banned {member} for {reason}.", mention_author=False)

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = "No reason provided."):
      if member is None:
          await ctx.reply(
              embed=self.bot.generate_embed("An error occured", "You need to provide a member to kick."),
              mention_author=False
          )
          return
      await member.kick(reason=reason)
      await ctx.reply(f"Kicked {member} for {reason}.", mention_author=False)

    @commands.command()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int=None):
        limit = limit or 100
        messages = await ctx.channel.purge(limit=limit)
        await ctx.send(f"{len(messages)} messages deleted.", delete_after=15)

def setup(bot: commands.AutoShardedBot) -> None:
    bot.add_cog(Moderation(bot))
