
# Write two Python functions: create_user and login_user.

# For create_user:
# It should accept db, username, and password as arguments.
# Use bcrypt to generate a salt and hash the provided password.
# Store the username and the decoded (utf-8) hashed password into a users table in the database.
# Ensure the database changes are committed.
# Return a dictionary indicating success and the username.

# For login_user:

# It should accept db, username, and password as arguments.
# Fetch the stored password for the given username from the users table.
# If the user is not found, return a failure status.
# Implement backward compatibility:
# If the stored_password is already a bcrypt hash (starts with $2a$, $2b$, or $2y$), verify it using bcrypt.checkpw.
# If the stored_password is plain text, compare it directly. If it matches, immediately hash the plain-text password with bcrypt and update the user's record in the database. Commit this update.
# Return a dictionary indicating success or failure, and for upgraded users, include an upgraded: True flag.

import bcrypt

def create_user(db, username, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed.decode('utf-8'))
    )
    db.commit()
    return {"status": "success", "user": username}

def login_user(db, username, password):
    cursor = db.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    if not row:
        return {"status": "failure", "reason": "User not found"}

    stored_password = row[0]
    # Check if stored_password is a bcrypt hash
    if stored_password.startswith(('$2a$', '$2b$', '$2y$')):
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return {"status": "success", "user": username}
        else:
            return {"status": "failure", "reason": "Incorrect password"}
    else:
        # Plain text password (backward compatibility)
        if password == stored_password:
            # Upgrade to bcrypt
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            db.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hashed.decode('utf-8'), username)
            )
            db.commit()
            return {"status": "success", "user": username, "upgraded": True}
        else:
            return {"status": "failure", "reason": "Incorrect password"}

