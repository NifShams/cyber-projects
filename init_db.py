import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Creating a users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Insert some default users
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'mypassword')")

conn.commit()
conn.close()

print("Database initialized successfully.")

