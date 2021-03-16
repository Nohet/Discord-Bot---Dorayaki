import os
import random
import string
from itertools import cycle

import DiscordUtils
import discord
from discord.ext import commands, tasks

from config import *
from database import *


def get_prefix(client, message):
    results = guildsett.find_one({"_id": message.guild.id})
    prefix = results["prefix"]
    return prefix


client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")

music = DiscordUtils.Music()


status = cycle(
    ['Try >help', 'Default prefix: > '])


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction("❌")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You can only use this command in server!")


@client.event
async def on_guild_join(guild):
    prefixguild = {"_id": guild.id, "prefix": ">", "muteRole": "Muted", "maxwarns": 3, "language": "en", "currency": "$"}
    guildsett.insert_one(prefixguild)


@client.event
async def on_ready():
    change_status.start()

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
@commands.guild_only()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )

    embed.set_author(name="Help")
    embed.add_field(name="Fun", value=f"``{help1}``", inline=False)
    embed.add_field(name="Economy", value=f"``{help2}``", inline=False)
    embed.add_field(name="Emotes", value=f"``{help3}``", inline=False)
    embed.add_field(name="Gambling", value=f"``{help4}``", inline=False)
    embed.add_field(name="Utility", value=f"``{help5}``", inline=False)
    embed.add_field(name="Music", value=f"``{help6}``")
    embed.set_footer(text=f"Invoked by {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)



for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

client.run(bot_token)
