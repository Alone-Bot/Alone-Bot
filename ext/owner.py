from __future__ import annotations
from typing import Optional

import discord
from discord.ext import commands

LOG = 907363405466333274
REDTICK_MARK = discord.PartialEmoji(name="redTick", id=596576672149667840)


class Owner(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def maintenance(self, ctx: commands.Context, *, reason: str = "No reason provided.") -> None:
      if not self.bot.maintenance:
          await ctx.message.add_reaction("\U00002705")
          self.bot.maintenance = True
          self.bot.maintenance_reason = reason
          channel = self.bot.get_channel(LOG)
          await channel.send("I am going on maintenance break, all commands will not work during the downtime.")
          return

      await ctx.reply("Maintenance break is over.", mention_author=False)
      channel = self.bot.get_channel(LOG)
      await channel.send("The maintenance break is over. You can use me again.")
      self.bot.maintenance = False
      self.bot.maintenance_reason = ""

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx: commands.Context) -> None:
        for user in self.bot.userblacklist:
            reason = user["reason"]
            profile = "".join(f"{user}, {reason}\n")
        await ctx.reply(embed=self.bot.generate_embed("Blacklisted users", profile), mention_author=False)

    @blacklist.command()
    async def add(self, ctx: commands.Context, user: discord.Member, *, reason: str = "No reason provided"):
        self.bot.userblacklist[user.id] = reason
        await ctx.message.add_reaction("\U00002705")

    @blacklist.command()
    async def remove(self, ctx: commands.Context, user: discord.Member) -> None:
        try:
            self.userblacklist.pop(user.id)
        except KeyError:
            await ctx.message.add_reaction("\U0000274c")
            return await ctx.reply("That user isn't blacklisted!", mention_author=False)
        else:
            return await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def disable(self, ctx: commands.Context, command: str):
        command = self.bot.get_command(command)
        if not command.enabled:
            await ctx.message.add_reaction(REDTICK_MARK)
            return await ctx.reply("This command is already disabled!", mention_author=False)
        command.enabled = False
        await ctx.message.add_reaction("\U00002705")
        await ctx.reply(f"Disabled {command}.", mention_author=False)

    @commands.command()
    async def enable(self, ctx: commands.Context, command: str):
        command = self.bot.get_command(command)
        if command.enabled:
          await ctx.message.add_reaction("\U00002705")
          return await ctx.reply("This command is already enabled!", mention_author=False)
        command.enabled = True
        await ctx.message.add_reaction("\U00002705")
        await ctx.reply(f"Enabled {command}.", mention_author=False)

    @commands.command(name="print")
    async def _print(self, ctx: commands.Context, *, arg: str = None):
        if not arg:
          await ctx.message.add_reaction(REDTICK_MARK)
          await ctx.reply("Why are you trying to print nothing? why?", mention_author=False)
        print(arg)
        await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def say(self, ctx: commands.Context, *, arg: str = None):
        if not arg:
            await ctx.message.add_reaction(REDTICK_MARK)
            return await ctx.reply("You have to give me something to say.", mention_author=False)
        await ctx.message.add_reaction("\U00002705")
        await ctx.reply(arg, mention_author=False)

    @commands.command(aliases=["d", "delete"])
    async def delmsg(self, ctx: commands.Context, message_id: Optional[int]=None):
        if not message_id:
            await ctx.message.add_reaction(REDTICK_MARK)
            return await ctx.reply("You need to give me a message to delete.", delete_after=10, mention_author=False)
        msg = ctx.channel.get_partial_message(message_id)
        await msg.delete()
        await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def nick(self, ctx: commands.Context, *, name: str = None):
        if not name:
            await ctx.me.edit(nick=None)
            await ctx.message.add_reaction("\U00002705")
        await ctx.me.edit(nick=name)
        await ctx.message.add_reaction("\U00002705")

    @commands.command(aliases=["log", "die", "shutdown", "fuckoff"])
    async def logout(self, ctx: commands.Context) -> None:
        await ctx.message.add_reaction("\U00002705")
        await ctx.bot.close()

    @commands.command()
    async def leave(self, ctx: commands.Context, guild_id: Optional[int] = None):
        if not guild_id:
            await ctx.message.add_reaction("\U00002705")
            await ctx.guild.leave()

        await self.bot.get_guild(guild_id).leave()
        await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def reload(self, ctx: commands.Context) -> None:
        for cog in self.bot.extensions.copy():
            self.bot.reload_extension(cog)
        await ctx.message.add_reaction("\U00002705")

def setup(bot: commands.AutoShardedBot) -> None:
    bot.add_cog(Owner(bot))
