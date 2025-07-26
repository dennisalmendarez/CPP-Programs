# user_auth.py
# This script handles user authentication for the Clipper Uploader application.
# It allows users to register, login, and securely store their credentials in a MongoDB database
# using hashed passwords.
import pymongo
import getpass
import hashlib
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the MONGO_URI environment variable is set
MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client["Users"]
accounts = db["Accounts"]

# Function to hash passwords using SHA-256
# This function takes a password string, encodes it, and returns the SHA-256 hash
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Register a new user
def register():
    username = input("🆕 New username: ")
    if accounts.find_one({"username": username}):
        print("❌ Username already exists.")
        return False
    # Use getpass.getpass to securely input password after finish test
    password = input("🔑 New password: ")
    accounts.insert_one({"username": username, "password": hash_password(password)})
    print("✅ Registered successfully!")
    return True

# Login an existing user
def login():
    username = input("👤 Username: ")
    user = accounts.find_one({"username": username})
    if not user:
        print("❌ User not found.")
        return False
    # Use getpass.getpass to securely input password after finish test
    password = input("🔑 Password: ")
    if user["password"] == hash_password(password):
        print("✅ Login successful.")
        return True
    else:
        print("❌ Incorrect password.")
        return False

# Update username and password functions
# These functions allow users to change their username securely
def update_username():
    username = input("👤 Current username: ")
    password = input("🔑 Password: ")
    user = accounts.find_one({"username": username})
    if not user or user["password"] != hash_password(password):
        print("❌ Invalid credentials.")
        return
    new_username = input("✏️ New username: ")
    if accounts.find_one({"username": new_username}):
        print("❌ That username is taken.")
        return
    accounts.update_one({"username": username}, {"$set": {"username": new_username}})
    print("✅ Username updated.")

# Update password function
# This function allows users to change their password securely
def update_password():
    username = input("👤 Username: ")
    old_pw = input("🔑 Current password: ")
    user = accounts.find_one({"username": username})
    if not user or user["password"] != hash_password(old_pw):
        print("❌ Invalid credentials.")
        return
    new_pw = input("🔐 New password: ")
    accounts.update_one({"username": username}, {"$set": {"password": hash_password(new_pw)}})
    print("✅ Password updated.")

# Delete account function
# This function allows users to delete their account securely
def delete_account():
    username = input("👤 Username: ")
    password = input("🔑 Password: ")
    user = accounts.find_one({"username": username})
    if not user or user["password"] != hash_password(password):
        print("❌ Invalid credentials.")
        return
    confirm = input("⚠️ Are you sure you want to delete this account? (yes/no): ")
    if confirm.lower() == "yes":
        accounts.delete_one({"username": username})
        print("🗑️ Account deleted.")
    else:
        print("❎ Canceled.")

def main():
    while True:
        print("\n[1] Login\n[2] Register\n[3] Exit\n[4] Update Username\n[5] Update Password\n[6] Delete Account")
        choice = input("Choose: ")
        if choice == "1":
            if login():
                sys.exit(0)
        elif choice == "2":
            register()
        elif choice == "3":
            sys.exit(2)
        elif choice == "4":
            update_username()
        elif choice == "5":
            update_password()
        elif choice == "6":
            delete_account()
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()