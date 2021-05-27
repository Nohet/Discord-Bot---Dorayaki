import os
from itertools import cycle
import time

import discord
from discord.ext import commands, tasks

from config import *
from database import *
from decorators import get_prefix

start_time = time.time()

intents = discord.Intents.default()

intents.members = True

client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.remove_command("help")

randomdata = ["tails", "heads"]

status = cycle(
    ['Try >help', 'Default prefix: > '])


@client.event
async def on_guild_join(guild):
    guildSettings = {"_id": guild.id, "prefix": ">", "muterole": "Muted", "maxwarns": 3, "language": "en",
                     "currency": "$", "logs": "disable", "logsChannel": None, "autorole": "disable",
                     "autoroleRole": None, "leave_messages": "disable", "join_messages": "disable",
                     "leave_messages_channel": None, "join_messages_channel": None,
                     "leave_messages_content": None, "join_messages_content": None,
                     "leave_messages_type": None, "join_messages_type": None}
    guildsett.insert_one(guildSettings)


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
    help1_list = help1.split(", ")
    help2_list = help2.split(", ")
    help3_list = help3.split(", ")
    help4_list = help4.split(", ")
    help5_list = help5.split(", ")
    help6_list = help6.split(", ")
    commands_number = len(help1_list) + len(help2_list) + len(help3_list) + len(help4_list) + len(help5_list) + len(help6_list)
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.set_author(name=f"Help | {commands_number} commands")
    embed.add_field(name=f"Economy ({len(help1_list)})", value=f"`{help1}`", inline=False)
    embed.add_field(name=f"Moderation ({len(help2_list)})", value=f"`{help2}`", inline=False)
    embed.add_field(name=f"Usefull ({len(help3_list)})", value=f"`{help3}`", inline=False)
    embed.add_field(name=f"Fun commands ({len(help4_list)})", value=f"`{help4}`", inline=False)
    embed.add_field(name=f"Automod ({len(help5_list)})", value=f"`{help5}`", inline=False)
    embed.add_field(name=f"Greetings ({len(help6_list)})", value=f"`{help6}`", inline=False)
    await ctx.send(embed=embed)


for directory in os.listdir("./Cogs"):
    for filename in os.listdir(f"./Cogs/{directory}"):
        if filename.endswith(".py"):
            client.load_extension(f"Cogs.{directory}.{filename[:-3]}")
            print(f"Successfully loaded {filename} ({directory})")


client.run(bot_token)
