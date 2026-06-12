from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["testdb"]

users_collection = db["Users"]