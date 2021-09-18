import discord
from discord.ext import commands
from discord.ext.commands.core import command 
from ext.useful import generate_embed

cogs = ["ext.essential","ext.owner","ext.moderation","ext.error","ext.sql"]
for cogs in cogs:
 
 def generate_button(int, content):
  button = discord.ui.View()
  if int == 1:
   style = discord.ButtonStyle.grey
  elif int == 2:
   style = discord.ButtonStyle.green
  elif int == 3:
   style = discord.ButtonStyle.red
  elif int == 4:
   style = discord.ButtonStyle.blurple
  elif int == 5:
   style = discord.ButtonStyle.url
  item = content
  return view

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def disable(self, ctx, command):
    command = self.bot.get_command(command)
    if not command.enabled:
      return await ctx.reply(embed=generate_embed("Disable", "This command is already disabled.","Disable | Alone Bot"), mention_author=False, delete_after=5)
    command.enabled = False
    await ctx.reply(embed=generate_embed("Disable",f"Disabled {command.name} command.","Disable | Alone Bot"), mention_author=False, delete_after=5)
  
  @commands.command()
  @commands.is_owner()
  async def say(self, ctx, *, arg=None):
   if arg is None:
    await ctx.reply(embed=generate_embed("You know what went wrong","You need to give me a message","Say | Alone Bot"), mention_author=False)
   else:
     await ctx.reply(embed=generate_embed(f"{arg}",f"{arg}","Say | Alone Bot"), mention_author=False)
  
  @commands.command()
  @commands.is_owner()
  async def enable(self, ctx, command):
    command = self.bot.get_command(command)
    if command.enabled:
      return await ctx.reply(embed=generate_embed("Enable", "This command is already enabled.","Enable | Alone Bot"), mention_author=False, delete_after=5)
    command.enabled = True
    await ctx.reply(embed=generate_embed("Enable",f"Enabled {command.name} command.","Enable | Alone Bot"), mention_author=False, delete_after=5)

  @commands.command(aliases=["r"])
  @commands.is_owner()
  async def reload(self, ctx):
   await ctx.reply(embed=generate_embed("Reloaded all Cogs!","Reloaded all cogs!","Cogs | Alone Bot", "0C9027"), mention_author=False, delete_after=5)
   self.bot.reload_extension(cogs)
  
  @commands.command(aliases=["delete", "msgdel"])
  @commands.is_owner()
  async def delmsg(self, ctx, msgid=None):
   if msgid is None:
    await ctx.send("You need to give me an id.")
   else:
    channel = ctx.channel
    msg = await channel.fetch_message(msgid)
    await msg.delete()
    await ctx.send("Done")
  
  @commands.command()
  @commands.is_owner()
  async def nick(self, ctx, *, name=None):
   if name == None:
    await ctx.me.edit(nick=None)
    await ctx.reply(embed=generate_embed("Roger", "My nickname has been reset.", "Alone Bot"), mention_author=False)
   else:
    await ctx.me.edit(nick=name)
    await ctx.reply(embed=generate_embed("I have changed my identity", f"My new nick is \"{name}\".", "Alone Bot"), mention_author=False)
  
  @commands.command(aliases=["log","die","shutdown","fuckoff","dios"])
  @commands.is_owner()
  async def logout(self, ctx):
   await ctx.reply(embed=generate_embed("Logout","Logging out now...","Logout | Alone Bot"), mention_author=False, delete_after=5)
   await ctx.bot.close()

  @commands.command(hidden=True)
  @commands.is_owner()
  async def cogsave(self, ctx):
   await self.bot.load_extension(cogs)
   await ctx.send("done")

  @commands.command(hidden=True)
  @command.is_owner()
  async def devkill(self, ctx):
   await ctx.send("cya")
   await self.bot.close()
 
def setup(bot):
  bot.add_cog(Owner(bot))
