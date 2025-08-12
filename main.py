def login_user(username, password):
    user = db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        return {"status": "failure", "reason": "User not found"}

    stored_password = user[0]

    # Check if stored password is a bcrypt hash (starts with $2b$, $2a$, or $2y$)
    if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return {"status": "success", "user": username}
        else:
            return {"status": "failure", "reason": "Incorrect password"}
    else:
        # Legacy plain-text password
        if password == stored_password:
            # Upgrade to bcrypt hash
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            db.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            return {"status": "success", "user": username, "upgraded": True}
        else:
            return {"status": "failure", "reason": "Incorrect password"}