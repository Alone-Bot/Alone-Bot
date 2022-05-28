import discord
from discord.ext import commands

from datetime import datetime
from typing import Optional, Dict

import os
from dotenv import load_dotenv
load_dotenv()

class Help(commands.HelpCommand):
  async def get_command_signature(self, command):
    return "%s %s" % (command.qualified_name, command.signature)

  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help", description="Use help (command) or help (category) for more information\n <> is a required argument | [] is an optional argument", color=discord.Color.blurple())
    embed.set_footer(text=f"Command ran by {self.context.author.display_name}", icon_url=self.context.author.avatar_url)
    embed.timestamp = datetime.utcnow()
    for cog, command in mapping.items():
      filtered = await self.filter_commands(command, sort=True)
      command_signatures = [await self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value=" ".join(command_signatures), inline=False)
    await self.context.reply(embed=embed, mention_author=False)
     
  async def send_command_help(self, command):
    commandname = await self.get_command_signature(command)
    embed = discord.Embed(title=commandname)
    embed.add_field(name="Description of the command", value=command.help)
    alias = command.aliases
    if alias:
      embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
    await self.context.reply(embed=embed, mention_author=False)

  async def send_error_message(self, error):
    embed = discord.Embed(title="Error", description=error)
    await self.context.reply(embed=embed, mention_author=False)

  async def send_group_help(self, group):
    embed = discord.Embed(title=group)
    embed.add_field(name="Subcommands", value=", ".join([command.name for command in group.walk_commands()]))
    await self.context.reply(embed=embed, mention_author=False)

  async def send_cog_help(self, cog):
    embed = discord.Embed(title=cog.qualified_name, description=cog.description)
    embed.add_field(name="Commands", value="\n".join(cog.get_commands()))
    await self.context.reply(embed=embed, mention_author=False)

#class DeleteButton(discord.Button):
#  def __init__(self):
#    self.style = discord.ButtonStyle.red()
#    self.label = "Delete"

class AloneContext(commands.Context):
  async def send(self, *args, **kwargs):
    if kwargs.get("embed"):
      if kwargs.get("embed").color:
        kwargs["embed"].color = discord.Color.random()
      else:
        kwargs["embed"].color = int(kwargs["embed"].color, 16)

    for embed in kwargs.get("embeds", []):
      if not embed.color:
        embed.color = discord.Color.random()

    return await super().send(*args, **kwargs)

  async def reply(self, *args, **kwargs):
    if not kwargs.get("mention_author"):
      kwargs["mention_author"] = False

    return await super().reply(*args, **kwargs)

class AloneBot(commands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.userblacklist: Dict[int, str] = {}
    self.afk: Dict[int, str] = {}
    self.maintenance = False
    self.maintenance_reason = ""
    self.command_counter = 0
    self.launch_time = datetime.utcnow()
    self.support_server = "https://discord.gg/kFkAmqhm"

  async def get_context(self, message, *, cls=AloneContext):
    return await super().get_context(message, cls=cls)

  def botmsgs(self, msg):
    return msg.author == self.user

class BlacklistedError(commands.CheckFailure):
  pass

class MaintenanceError(commands.CheckFailure):
  pass

os.environ["JISHAKU_HIDE"] = "true"
os.environ["JISHAKU_RETAIN"] = "true"
os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "true"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"

bot = AloneBot(
  command_prefix="owo",
  intents=discord.Intents.all(),
  activity=discord.Game("with my Source Code"),
  strip_after_prefix=True,
  case_insensitive=True,
  owner_ids=[349373972103561218, 412734157819609090, 755055117773963476],
 )

bot.load_extension("jishaku")
initial_extensions = [
  "ext.error",
  "ext.events",
  "ext.fun",
  "ext.help",
  "ext.moderation",
  "ext.owner",
  "ext.utility",
]
for cog in initial_extensions:
  bot.load_extension(cog)

@bot.after_invoke
async def aftercount(_: commands.Context):
  bot.command_counter += 1

@bot.check
def blacklist(ctx: commands.Context):
  if ctx.author.id not in bot.userblacklist:
    return True
  else:
    raise BlacklistedError

@bot.check
def maintenance(ctx: commands.Context):
  if bot.maintenance or ctx.author.id in bot.owner_ids:
    return True
  else:
    raise MaintenanceError

bot.run(os.getenv("token"))