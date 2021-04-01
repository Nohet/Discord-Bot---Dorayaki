import os
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
randomdata = ["tails", "heads"]

status = cycle(
    ['Try >help', 'Default prefix: > ', f'Currently in {len(client.guilds)} servers'])


@client.event
async def on_command_error(ctx, error):
    r = guildsett.find_one({"_id": ctx.guild.id})
    if isinstance(error, commands.CommandNotFound):
        r = guildsett.find_one({"_id": ctx.message.guild.id})
        getprefix = r["prefix"]
        getcommandname1 = r["1customcmdname"]
        getcommandname2 = r["2customcmdname"]
        getcommandname3 = r["3customcmdname"]
        getcommandname4 = r["4customcmdname"]
        getcommandname5 = r["5customcmdname"]
        if ctx.message.content == (f"{getprefix}{getcommandname1}"):
            return False
        elif ctx.message.content == (f"{getprefix}{getcommandname2}"):
            return False
        elif ctx.message.content == (f"{getprefix}{getcommandname3}"):
            return False
        elif ctx.message.content == (f"{getprefix}{getcommandname4}"):
            return False
        elif ctx.message.content == (f"{getprefix}{getcommandname5}"):
            return False
        else:
            await ctx.message.add_reaction("❌")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You can only use this command in server!")


@client.event
async def on_guild_join(guild):
    prefixguild = {"_id": guild.id, "prefix": ">", "muterole": "Muted", "maxwarns": 3, "language": "en", "currency": "$",
                   "nsfw": True, "customcmds": 5, "1customcmdname": None, "1customcmdtype": None, "1customcmdcontent": None,
                   "2customcmdname": None, "2customcmdtype": None, "2customcmdcontent": None,
                   "3customcmdname": None, "3customcmdtype": None, "3customcmdcontent": None,
                   "4customcmdname": None, "4customcmdtype": None, "4customcmdcontent": None,
                   "5customcmdname": None, "5customcmdtype": None, "5customcmdcontent": None}
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
    collection.update_one({"received": True}, {"$set": {"received": False}})


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
