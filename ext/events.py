from __future__ import annotations
import re

import discord
from discord.ext import commands

JOIN_LOG = 906682479199531051

class Events(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot
  
    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        channel = self.bot.get_channel(JOIN_LOG)
        bots = sum(m.bot for m in guild.members)
        joinembed = discord.Embed(
            title="I joined a new guild!", color=discord.Color(int("5fad68", 16)),
        )
        joinembed.description = f"""Owner: {guild.owner}
Name: {guild.name}
Members: {guild.member_count}
Bots: {bots}
Nitro Tier: {guild.premium_tier}
"""
        joinembed.set_footer(text="Alone Bot", icon_url=guild.icon_url)
        await channel.send(embed=joinembed)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild) -> None:
        channel = self.bot.get_channel(JOIN_LOG)
        await channel.send(f"I got kicked from {guild.name}.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if re.fullmatch(rf"<@!?{self.user.id}>", message.content):
            await message.channel.send("Hi, you just pinged me.")

    @commands.Cog.listener("on_message")
    async def is_afk_mention(self, message: discord.Message) -> None:
        for id in message.raw_mentions:
            for afkid in self.bot.afk.copy():
                if id == afkid and not message.author.bot:
                    await message.channel.send(f"I'm sorry, but <@{id}> went afk for {self.bot.afk[id]}.")

    @commands.Cog.listener("on_message")
    async def is_afk(self, message) -> None:
        for id in self.bot.afk.copy():
            if id == message.author.id:
                self.bot.afk.pop(message.author.id)
                await message.channel.send(f"Welcome back <@{id}>!")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        
        if before.author.bot:
            return

        await self.bot.process_commands(after)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Events(bot))
