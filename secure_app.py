from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify
import sqlite3
import bcrypt
import secrets
from markupsafe import escape

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a strong secret key

def get_db_connection():
    conn = sqlite3.connect('database_secure.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    """Create users table with hashed passwords"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

create_users_table()

def add_default_users():
    """Add default users to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if there are no users in the table
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Add default users with hashed passwords
        users = [
            ('admin', bcrypt.hashpw('admin_password'.encode(), bcrypt.gensalt())),
            ('user1', bcrypt.hashpw('password1'.encode(), bcrypt.gensalt())),
            ('user2', bcrypt.hashpw('password2'.encode(), bcrypt.gensalt())),
        ]
        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)
        conn.commit()
    
    conn.close()

add_default_users()


# Secure Login with Hashed Passwords
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user["password"]):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials.", 401
    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit">
    </form>
    '''

# Secure Comment Section (Prevents XSS)
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        comment = escape(request.form["comment"])  # Escape input to prevent XSS
        return f"Comment posted: {comment}"
    return '''
    <h2>Post a Comment</h2>
    <form method="POST">
        Comment: <input type="text" name="comment"><br>
        <input type="submit">
    </form>
    '''

# Secure Profile Access with Authorization Check
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = request.args.get("id")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ? AND username = ?", (user_id, session["user"]))
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"Profile: {user['username']}"
    return "Unauthorized access.", 403

# CSRF-Protected Money Transfer
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        csrf_token = request.form.get("csrf_token")
        if not csrf_token or csrf_token != session.get("csrf_token"):
            return "CSRF token missing or invalid.", 403

        amount = request.form["amount"]
        return f"Transferred {escape(amount)} successfully!"

    session["csrf_token"] = secrets.token_hex(16)  # Generate CSRF token
    return f'''
    <h2>Money Transfer</h2>
    <form method="POST">
        <input type="hidden" name="csrf_token" value="{session['csrf_token']}">
        Amount: <input type="text" name="amount"><br>
        <input type="submit">
    </form>
    '''

# Secure Dashboard with Proper Session Handling
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Welcome {session['user']}! <a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()  # Securely log out the user
    return redirect(url_for("login"))

# Prevent Open Redirect Attacks
@app.route("/redirect")
def open_redirect():
    allowed_domains = ["example.com", "mysecureapp.com"]
    url = request.args.get("url")

    if not url or any(domain in url for domain in allowed_domains):
        return redirect(url)
    return "Invalid redirect URL.", 400

# Secure Admin Panel
@app.route("/admin")
def admin():
    if "user" not in session or session["user"] != "admin":
        return "Access denied. Unauthorized!", 403
    return "Welcome to the Admin Panel!"

if __name__ == "__main__":
    app.run(debug=True)
