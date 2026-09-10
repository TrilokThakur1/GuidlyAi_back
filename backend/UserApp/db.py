from pymongo import MongoClient
from decouple import config

MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

db = client["testdb"]

users_collection = db["Users"]