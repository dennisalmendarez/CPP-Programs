import mysql.connector
import hashlib
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL"),
    ssl_disabled=True
)
cursor = conn.cursor(dictionary=True)

# Hash password
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Register a new user
def register():
    username = input("🆕 New username: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    if cursor.fetchone():
        print("❌ Username already exists.")
        return
    password = input("🔑 New password: ")
    cursor.execute(
        "INSERT INTO accounts (username, password) VALUES (%s, %s)",
        (username, hash_password(password))
    )
    conn.commit()
    print("✅ Registered successfully!")

# Login user
def login():
    username = input("👤 Username: ")
    password = input("🔑 Password: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user:
        print("❌ User not found.")
        return False
    if user["password"] == hash_password(password):
        print(f"✅ Login successful. Account created at: {user['created_at']}")
        return True
    print("❌ Incorrect password.")
    return False

# Update username
def update_username():
    username = input("👤 Current username: ")
    password = input("🔑 Password: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user or user["password"] != hash_password(password):
        print("❌ Invalid credentials.")
        return
    new_username = input("✏️ New username: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (new_username,))
    if cursor.fetchone():
        print("❌ That username is taken.")
        return
    cursor.execute("UPDATE accounts SET username=%s WHERE username=%s", (new_username, username))
    conn.commit()
    print("✅ Username updated.")

# Update password
def update_password():
    username = input("👤 Username: ")
    old_pw = input("🔑 Current password: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user or user["password"] != hash_password(old_pw):
        print("❌ Invalid credentials.")
        return
    new_pw = input("🔐 New password: ")
    cursor.execute("UPDATE accounts SET password=%s WHERE username=%s", (hash_password(new_pw), username))
    conn.commit()
    print("✅ Password updated.")

# Delete account
def delete_account():
    username = input("👤 Username: ")
    password = input("🔑 Password: ")
    cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user or user["password"] != hash_password(password):
        print("❌ Invalid credentials.")
        return
    confirm = input("⚠️ Are you sure you want to delete this account? (yes/no): ")
    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM accounts WHERE username=%s", (username,))
        conn.commit()
        print("🗑️ Account deleted.")
    else:
        print("❎ Canceled.")

# Show accounts within a date range
def show_accounts_by_date():
    start_date = input("📅 Start date (YYYY-MM-DD): ")
    end_date = input("📅 End date (YYYY-MM-DD): ")
    cursor.execute("""
        SELECT username, created_at 
        FROM accounts 
        WHERE DATE(created_at) BETWEEN %s AND %s
        ORDER BY created_at ASC
    """, (start_date, end_date))
    results = cursor.fetchall()
    if results:
        print("\n📋 Accounts in date range:")
        for row in results:
            print(f"- {row['username']} | Created at: {row['created_at']}")
    else:
        print("❌ No accounts found in that date range.")

# Menu
def main():
    while True:
        print("\n[1] Login\n[2] Register\n[3] Exit\n[4] Update Username\n[5] Update Password\n[6] Delete Account\n[7] Show Accounts by Date Range")
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
        elif choice == "7":
            show_accounts_by_date()
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()
