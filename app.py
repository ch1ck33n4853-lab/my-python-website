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

@app.route("/", methods=["GET"])
def home():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, message FROM guestbook ORDER BY id DESC")
        entries = cursor.fetchall()
    
    with open("index.html", "r") as f:
        html_content = f.read()
        
    return render_template_string(html_content, entries=entries)

@app.route("/submit", methods=["POST"])
def submit():
    # This reads the 'name' attributes from your HTML form fields instead of JSON
    username = request.form.get("username")
    message = request.form.get("message")
    
    if username and message:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO guestbook (name, message) VALUES (?, ?)", (username, message))
            conn.commit()
            
    return redirect("/")

if __name__ == "__main__":
    init_db()
