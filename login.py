from pymongo import MongoClient
import bcrypt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.ats_database
    users_collection = db.users

    # Check connection
    client.admin.command('ping')
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Authentication Functions
def create_user(email, password):
    """
    Registers a new user by hashing their password and storing them in MongoDB.
    """
    if users_collection.find_one({"email": email}):
        raise ValueError("Email already exists")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        "email": email,
        "password_hash": hashed,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow()
    }
    return users_collection.insert_one(user_data)

def verify_user(email, password):
    """
    Verifies user credentials for login.
    """
    user = users_collection.find_one({"email": email})
    if not user:
        return None
    if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        users_collection.update_one(
            {"_id": user['_id']},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return user
    return None
