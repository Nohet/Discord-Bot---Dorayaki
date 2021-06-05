import discord
from discord.ext import commands

import asyncpraw

import random
from decorators import is_nsfw_enabled

from config import reddit_client_id, reddit_client_secret, reddit_user_agent, reddit_username, reddit_post_limit

is_nsfw_enabled = commands.check(is_nsfw_enabled)

reddit = asyncpraw.Reddit(client_id=reddit_client_id,
                          client_secret=reddit_client_secret,
                          user_agent=reddit_user_agent,
                          username=reddit_username)


class GeneralNSFWCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_nsfw()
    @is_nsfw_enabled
    async def pussy(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Please wait!", value=f"Loading {reddit_post_limit} posts, this may take a while!")
        await ctx.send(embed=embed)

        subreddit = await reddit.subreddit("pussy")
        all_subs = []

        top = subreddit.top(limit=reddit_post_limit)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    @is_nsfw_enabled
    async def boobs(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Please wait!", value=f"Loading {reddit_post_limit} posts, this may take a while!")
        await ctx.send(embed=embed)

        subreddit = await reddit.subreddit("boobs")
        all_subs = []

        top = subreddit.top(limit=reddit_post_limit)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    @is_nsfw_enabled
    async def nsfw(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Please wait!", value=f"Loading {reddit_post_limit} posts, this may take a while!")
        await ctx.send(embed=embed)

        subreddit = await reddit.subreddit("nsfw")
        all_subs = []

        top = subreddit.top(limit=reddit_post_limit)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.is_nsfw()
    @is_nsfw_enabled
    async def thigh(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Please wait!", value=f"Loading {reddit_post_limit} posts, this may take a while!")
        await ctx.send(embed=embed)

        subreddit = await reddit.subreddit("thigh")
        all_subs = []

        top = subreddit.top(limit=reddit_post_limit)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    @is_nsfw_enabled
    async def anal(self, ctx):
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Please wait!", value=f"Loading {reddit_post_limit} posts, this may take a while!")
        await ctx.send(embed=embed)

        subreddit = await reddit.subreddit("anal")
        all_subs = []

        top = subreddit.top(limit=reddit_post_limit)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.set_author(name=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(GeneralNSFWCog(client))
