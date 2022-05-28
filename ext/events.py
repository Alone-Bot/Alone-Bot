from discord.ext import commands
import discord

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
 
  @commands.Cog.listener()
  async def on_ready(self):
    print("Connected")

  @commands.Cog.listener()
  async def on_guild_join(self, guild: discord.Guild):
    channel = self.bot.get_channel(906682479199531051) or self.bot.fetch_channel(906682479199531051)
    bots = sum(m.bot for m in guild.members)
    joinembed = discord.Embed(title="I joined a new guild!", description=f"Owner: {guild.owner}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: {guild.premium_tier}", color=discord.Color(int("5fad68", 16)))
    joinembed.set_footer(text="Alone Bot", icon_url=guild.icon_url)
    await channel.send(embed=joinembed)

  @commands.Cog.listener()
  async def on_guild_leave(self, guild: discord.Guild):
    channel = self.bot.get_channel(906682479199531051) or self.bot.fetch_channel(906682479199531051)
    await channel.send(f"I got kicked from {guild.name}.")

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if self.bot.user.id in message.mentions and not message.author.bot:
      await message.channel.send("Hi, you just pinged me.")

  @commands.Cog.listener("on_message")
  async def is_afk_mention(self, message: discord.Message):
    for _id in message.raw_mentions:
      for afkid in self.bot.afk.copy():
        if _id == afkid and not message.author.bot:
          await message.channel.send(f"I'm sorry, but <@{_id}> went afk for {self.bot.afk[_id]}.")

  @commands.Cog.listener("on_message")
  async def is_afk(self, message: discord.Message):
    for _id in self.bot.afk.copy():
      if _id == message.author.id:
        self.bot.afk.pop(message.author.id)
        await message.channel.send(f"Welcome back <@{_id}>!")

  @commands.Cog.listener()
  async def on_message_edit(self, _: discord.Message, after: discord.Message):
    await self.bot.process_commands(after)

def setup(bot):
  bot.add_cog(Events(bot))
