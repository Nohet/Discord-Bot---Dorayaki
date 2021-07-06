import json

from pymongo import MongoClient

with open("settings.json") as f:
    settings = json.load(f)

cluster = MongoClient(settings["bot settings"]["mongo_token"])
db = cluster["Discord"]

collection = db["economy"]
guildsett = db["settings"]
warnsdata = db["warns"]
