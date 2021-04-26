import os
from itertools import cycle
import requests

import DiscordUtils
import discord, time
from discord.ext import commands, tasks

from config import *
from database import *


def get_prefix(client, message):
    results = guildsett.find_one({"_id": message.guild.id})
    prefix = results["prefix"]
    return prefix


start_time = time.time()

client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")

music = DiscordUtils.Music()
randomdata = ["tails", "heads"]

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
    prefixguild = {"_id": guild.id, "prefix": ">", "muterole": "Muted", "maxwarns": 3, "language": "en",
                   "currency": "$"}
    guildsett.insert_one(prefixguild)


@client.event
async def on_ready():
    change_status.start()
    reset_reward.start()


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@tasks.loop(hours=24)
async def reset_reward():
    collection.update_many({"received": True}, {"$set": {"received": False}})


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.reload_extension(f"Cogs.{extension}")
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully reloaded {extension} module!")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Error", value=f"You don't have permissions to use this command!")
        await ctx.send(embed=embed)


@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.load_extension(f"Cogs.{extension}")
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully loaded {extension} module!")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Error", value=f"You don't have permissions to use this command!")
        await ctx.send(embed=embed)


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == owner_id:
        client.unload_extension(f"Cogs.{extension}")
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value=f"Successfully unloaded {extension} module!")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Error", value=f"You don't have permissions to use this command!")
        await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.set_author(name="Help")
    embed.add_field(name="Economy", value=f"`{help1}`", inline=False)
    embed.add_field(name="Moderation", value=f"`{help2}`", inline=False)
    embed.add_field(name="Usefull", value=f"`{help3}`", inline=False)
    embed.add_field(name="Fun commands", value=f"`{help4}`", inline=False)
    await ctx.send(embed=embed)


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

client.run(bot_token)
