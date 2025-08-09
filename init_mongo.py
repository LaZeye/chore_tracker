from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://192.168.0.247:27017/chore_tracker')
client = MongoClient(MONGO_URI)
db = client['chore_tracker']

db.chores.create_index([("status", 1), ("posted_by", 1)])
db.transactions.create_index([("user_id", 1), ("created_at", -1)])
db.balances.create_index([("user_id", 1)], unique=True)

print("MongoDB collections initialized.")
client.close()