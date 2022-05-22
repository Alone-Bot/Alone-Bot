from __future__ import annotations

import discord
from discord.ext import commands

from main import BlacklistedError, MaintenanceError

REDTICK_MARK = discord.PartialEmoji(name="redTick", id=596576672149667840)
ERROR_LOG = 906683175571435550


class Error(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        await ctx.message.add_reaction(REDTICK_MARK)

        if isinstance(error, BlacklistedError):
            reason = self.bot.blacklist.get(ctx.author.id)
            await ctx.reply(
                f"You have been blacklisted for {reason}. you may not appeal this blacklist. There still exists a chance I'll unban you, but it's not likely.",
                mention_author=False,
                delete_after=20
            )
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.reply(
                embed=self.bot.generate_embed(
                    ctx, "Error", "You do not have permission to run this command!", "ea132c"
                ),
                mention_author=False
              )
            return

        if isinstance(error, MaintenanceError):
            await ctx.reply(
                f"The bot is currently in maintenance mode for {self.bot.maintenance_reason}, please wait. If you have any issues, you can join my support server for help.",
                mention_author=False,
                delete_after=20
            )
            return
        
        errorembed = discord.Embed(
            title=f"Ignoring exception in {ctx.command}:",
            description=f"```py\n{error}```",
            color=discord.Color(int("FF2E2E", 16)),
            timestamp=ctx.message.created_at
        )

        channel = self.bot.get_channel(ERROR_LOG)
        await channel.send(f"This error came from {ctx.author} using `{ctx.command.qualified_name}` in {ctx.guild}.", embed=errorembed)

        await ctx.reply(embed=errorembed, mention_author=False, delete_after=120)


def setup(bot: commands.AutoShardedBot) -> None:
    bot.add_cog(Error(bot))