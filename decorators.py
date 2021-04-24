import discord
from database import *


async def is_registered(ctx):
    findacc = collection.find_one({"_id": ctx.author.id})
    if not findacc:
        usereconomy = {"_id": ctx.message.author.id, "wallet": 0, "bank": 0, "received": False}
        collection.insert_one(usereconomy)
        embed = discord.Embed(
            colour=discord.Color.from_rgb(244, 182, 89)
        )
        embed.add_field(name="Success", value="Successfully created account!")
        await ctx.send(embed=embed)
    return True
