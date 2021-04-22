from database import *


def is_registered(ctx):
    findacc = collection.find_one({"_id": ctx.author.id})
    if not findacc:
        usereconomy = {"_id": ctx.message.author.id, "wallet": 0, "bank": 0, "received": False}
        collection.insert_one(usereconomy)
    return True
