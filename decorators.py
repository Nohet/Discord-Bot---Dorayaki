import discord

from database import *


async def is_registered(ctx):
    findacc = collection.find_one({"_id": ctx.author.id})
    if not findacc:
        usereconomy = {"_id": ctx.message.author.id, "items": "None", "wallet": 0, "voice_time": 0, "bank": 0,
                       "received": False, "slots": 0, "coinflips": 0, "rob": 0, "horse_racing": 0}
        collection.insert_one(usereconomy)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value="Successfully created account!")
        await ctx.send(embed=embed)
    return True


async def get_prefix(client, message):
    results = guildsett.find_one({"_id": message.guild.id})
    prefix = results["prefix"]
    return prefix


async def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


async def is_disabled(ctx):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(244, 182, 89)
    )
    embed.add_field(name="Error", value="This command is disabled!")
    await ctx.send(embed=embed)
    return False


