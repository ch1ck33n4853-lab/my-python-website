import sqlite3
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
DB_FILE = "database.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS guestbook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route("/", methods=["GET", "HEAD"])
def home():
    # Force initialize the database right here so it never errors out on page load
    init_db()
    
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, message FROM guestbook ORDER BY id DESC")
            entries = cursor.fetchall()
    except Exception:
        entries = []
    
    # Safely look for your HTML template file
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            html_content = f.read()
    else:
        html_content = "<h1>My Corner</h1><p>index.html was not found in directory.</p>"
        
    return render_template_string(html_content, entries=entries)

@app.route("/submit", methods=["POST"])
def submit():
    init_db()
    username = request.form.get("username")
    message = request.form.get("message")
    
    if username and message:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO guestbook (name, message) VALUES (?, ?)", (username, message))
            conn.commit()
            
    return redirect("/")

if __name__ == "__main__":
    init_db()

