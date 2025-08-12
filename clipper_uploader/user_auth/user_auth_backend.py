import pymongo
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["Users"]
accounts = db["Accounts"]

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def update_username_backend(current_username, password, new_username):
    user = accounts.find_one({"username": current_username})
    if not user or user["password"] != hash_password(password):
        return False, "Invalid current username or password."
    if accounts.find_one({"username": new_username}):
        return False, "That new username is already taken."
    accounts.update_one({"username": current_username}, {"$set": {"username": new_username}})
    return True, "Username updated successfully."

def update_password_backend(username, old_password, new_password):
    user = accounts.find_one({"username": username})
    if not user or user["password"] != hash_password(old_password):
        return False, "Invalid username or current password."
    accounts.update_one({"username": username}, {"$set": {"password": hash_password(new_password)}})
    return True, "Password updated successfully."

def delete_account_backend(username, password):
    user = accounts.find_one({"username": username})
    if not user or user["password"] != hash_password(password):
        return False, "Invalid username or password."
    accounts.delete_one({"username": username})
    return True, "Account deleted successfully."