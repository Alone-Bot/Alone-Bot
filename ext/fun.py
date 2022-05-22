from __future__ import annotations
import string
from typing import Any, Dict

import discord
import random
import aiohttp
import sr_api
import asyncpraw
import os
from discord.ext import commands
from waifuim import WaifuAioClient
from datetime import datetime

async def urban(word: str) -> Dict[str, Any]:
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
    def __init__(self, bot: commands.AutoShardedBot) -> None:
      self.bot = bot

    @commands.command(aliases=["define"])
    async def urban(self, ctx: commands.Context, *, word: str) -> None:
        data = await urban(word)
        if not data:
            return await ctx.reply("No results, sorry!", mention_author=False)
        definition = data["list"][0]["definition"]
        name = data["list"][0]["word"]
        await ctx.reply(
            embed=self.bot.generate_embed(ctx, name, definition), mention_author=False
        )

    @commands.command()
    async def token(self, ctx: commands.Context) -> None:
        at = await srapi.encode_base64(
            f"{int(ctx.message.created_at.timestamp()) + 1923840000}"
        )
        _id = await srapi.encode_base64(str(ctx.author.id))
        letters_numbers = f"{string.ascii_letters}{string.digits}"
        enc = "".join((random.choice(letters_numbers) for i in range(27)))
        await ctx.reply(
            embed=self.bot.generate_embed(
                ctx, "Here's your token!", f"Hey {ctx.author.mention}, here's your randomly generated token!\n`{_id}.{at}.{enc}`"
            ),
            mention_author=False
        )
    
    @commands.command()
    async def pp(self, ctx: commands.Context, member: discord.Member = None) -> None:
        member = member or ctx.author
        ppsize = random.randint(1, 50)
        pp = "".join("=" * ppsize)
        await ctx.reply(
            embed=self.bot.generate_embed(
                ctx, f"{member}'s pp", f"8{pp}D\n({ppsize}cm)"
            ),
            mention_author=False
        )

    @commands.command()
    async def meme(self, ctx: commands.Context):
        subreddit = await reddit.subreddit("dankmemes")
        meme = random.choice([post async for post in subreddit.new(limit=250)])
        embed = discord.Embed().set_image(url=meme.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def joke(self, ctx: commands.Context):
        joke = await srapi.get_joke()
        await ctx.reply(embed=self.bot.generate_embed(ctx, "Joke", joke), mention_author=False)

    @commands.command()
    async def waifu(self, ctx: commands.Context):
        waifu_url = await hori.random(is_nsfw=["False"], selected_tags=["waifu"])
        embed = discord.Embed(
            title=f"Here's your waifu, {ctx.author.name}", description=f"[Here's the link]({waifu_url})"
        )
        embed.set_footer(
            text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url
        )
        embed.set_image(url=waifu_url)
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot: commands.AutoShardedBot) -> None:
    bot.add_cog(Fun(bot))
