from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://192.168.0.247:27017/chore_tracker')
client = MongoClient(MONGO_URI)
db = client['chore_tracker']

try:
    users = db.users.find()
    print("Users in chore_tracker database:")
    for user in users:
        print(f"Name: {user['name']}, Role: {user['role']}")
except Exception as e:
    print(f"Error querying MongoDB: {e}")
finally:
    client.close()