from pymongo import MongoClient
from config import mongo_token

cluster = MongoClient(mongo_token)
db = cluster["Discord"]

collection = db["economy"]
guildsett = db["settings"]
warnsdata = db["warns"]
