import json

from pymongo import MongoClient

with open("./settings.json") as f:
    bot_settings = json.load(f)

cluster = MongoClient(bot_settings["bot settings"]["mongo_token"])
db = cluster["Discord"]

economy = db["economy"]
settings = db["settings"]
warns = db["warns"]
