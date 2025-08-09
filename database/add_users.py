from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://192.168.0.247:27017/chore_tracker')
client = MongoClient(MONGO_URI)
db = client['chore_tracker']

users = [
    {'name': 'Dad', 'role': 'Parent', 'password': generate_password_hash('dad123')},
    {'name': 'Mom', 'role': 'Parent', 'password': generate_password_hash('mom123')},
    {'name': 'Grant', 'role': 'Kid', 'password': generate_password_hash('gcd')},
    {'name': 'Grayson', 'role': 'Kid', 'password': generate_password_hash('grayson123')}
]

db.users.drop()  # Clear existing users
db.users.insert_many(users)
print("Users added:", [u['name'] for u in db.users.find()])
client.close()