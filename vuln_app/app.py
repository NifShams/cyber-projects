from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Hardcoded secret key (Security risk!)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# SQL Injection Vulnerability
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)  # Vulnerable to SQL Injection
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials."
    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit">
    </form>
    '''

# Cross-Site Scripting (XSS) Vulnerability
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        comment = request.form["comment"]  # No sanitization (XSS vulnerability)
        return f"Comment posted: {comment}"
    return '''
    <h2>Post a Comment</h2>
    <form method="POST">
        Comment: <input type="text" name="comment"><br>
        <input type="submit">
    </form>
    '''

# Insecure Direct Object Reference (IDOR) Vulnerability
@app.route("/profile")
def profile():
    user_id = request.args.get("id")  # No authorization check
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return f"Profile: {user['username']}"
    return "User not found."

# CSRF Vulnerability
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        if "user" not in session:
            return "Please log in first."
        amount = request.form["amount"]  # No CSRF token verification
        return f"Transferred {amount} successfully!"
    return '''
    <h2>Money Transfer</h2>
    <form method="POST">
        Amount: <input type="text" name="amount"><br>
        <input type="submit">
    </form>
    '''

# Broken Authentication
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # No proper session handling
    return f"Welcome {session['user']}! <a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Open Redirect Vulnerability
@app.route("/redirect")
def open_redirect():
    url = request.args.get("url")  # No validation of the URL
    return redirect(url)

# Admin Panel (Insecure Authorization Bypass)
@app.route("/admin")
def admin():
    if "user" not in session or session["user"] != "admin":
        return "Access denied. Unauthorized!"
    return "Welcome to the Admin Panel! (This page is vulnerable to session hijacking)"

if __name__ == "__main__":
    app.run(debug=True)
