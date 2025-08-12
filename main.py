import sqlite3
from user_service import create_user, login_user

# In-memory SQLite DB for demonstration
db = sqlite3.connect(":memory:")

# Create users table
db.execute("CREATE TABLE users (username TEXT, password TEXT)")
db.commit()

# --- Simulate vulnerable state: insert a plaintext user ---
db.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("alice", "plaintext123"))
db.commit()

# First login with plaintext password — should succeed and upgrade to bcrypt
print("=== First Login (plaintext password) ===")
result_first = login_user(db, "alice", "plaintext123")
print(result_first)

# Second login with bcrypt hash — should succeed without upgrade
print("\n=== Second Login (already hashed) ===")
result_second = login_user(db, "alice", "plaintext123")
print(result_second)

# Attempt login with wrong password
print("\n=== Login Attempt with Wrong Password ===")
result_wrong = login_user(db, "alice", "wrongpass")
print(result_wrong)

# Attempt login with non-existent user
print("\n=== Login Attempt for Non-Existent User ===")
result_no_user = login_user(db, "bob", "somepass")
print(result_no_user)
