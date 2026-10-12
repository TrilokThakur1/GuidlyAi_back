from pymongo import MongoClient
from decouple import config

MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

db = client["testdb"]

users_collection = db["Users"]

# Ensure index on email for instant O(1) lookup
try:
    users_collection.create_index("email", background=True)
except Exception as e:
    print("Notice: Index on Users email setup skipped:", str(e))
