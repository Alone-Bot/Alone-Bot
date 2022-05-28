import discord, asyncpg, random, aiohttp, sr_api, asyncpraw, base64, os
from discord.ext import commands
from waifuim import WaifuAioClient
from datetime import datetime

async def urban(word: str):
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://api.urbandictionary.com/v0/define?term={word}") as word:
			response = await word.json()
	return response

srapi = sr_api.Client()
hori = WaifuAioClient(session=aiohttp.ClientSession(), appname="Alone Bot")

reddit = asyncpraw.Reddit(
  client_id=os.getenv("client_id"),
  client_secret=os.getenv("client_secret"),
  user_agent=os.getenv("user_agent"),
  username=os.getenv("username"),
)

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["define"])
  async def urban(self, ctx, *, word: str):
    d = await urban(word)
    if not d:
      return await ctx.reply("No results, sorry!")
    definition = d["list"][0]["definition"]
    name = d["list"][0]["word"]
    await ctx.reply(embed=discord.Embed(title=name, description=definition))

  @commands.command()
  async def token(self, ctx):
    time = await srapi.encode_base64(str(int(datetime.utcnow().timestamp()) + 1923840000))
    _id = await srapi.encode_base64(str(ctx.author.id))
    _range = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    enc = "".join((random.choice(_range) for i in range(27)))
    await ctx.reply(embed=discord.Embed(
      title="Here's your token!",
      description=f"Hey {ctx.author.mention}, here's your randomly generated token!\n`{_id}.{time}.{enc}`"
      ))
  
  @commands.command()
  async def pp(self, ctx, member: discord.Member = None):
    if member is None:
      member = ctx.author
    ppsize = random.randint(1, 50)
    pp = "".join("=" * ppsize)
    await ctx.reply(embed=discord.Embed(title=f"{member}'s pp", description=f"8{pp}D\n({ppsize}cm)"))

  @commands.command()
  async def meme(self, ctx):
    subreddit = await reddit.subreddit("dankmemes")
    meme = random.choice([post async for post in subreddit.new(limit=250)])
    embed = discord.Embed().set_image(url=meme.url)
    await ctx.reply(embed=embed)

  @commands.command()
  async def joke(self, ctx):
    joke = await srapi.get_joke()
    await ctx.reply(embed=discord.Embed(title="Joke", description=joke))

  @commands.command()
  async def waifu(self, ctx):
    waifu_url = await hori.random(is_nsfw=["False"], selected_tags=["waifu"])
    embed = discord.Embed(title=f"Here's your waifu, {ctx.author.name}", description=f"[Here's the link]({waifu_url})")
    embed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed.set_image(url=waifu_url)
    await ctx.reply(embed=embed)

def setup(bot):
  bot.add_cog(Fun(bot))
