import sqlite3
import os
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)
DB_FILE = "database.db"

# Initialize SQLite database and create a table for messages
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            )
        """)
        conn.commit()

# Serve your existing index.html file
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

# An example API endpoint to save data to SQLite from your site
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}
    message_text = data.get("message")
    
    if message_text:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO messages (text) VALUES (?)", (message_text,))
            conn.commit()
        return jsonify({"status": "success", "message": "Saved to SQLite!"})
    
    return jsonify({"status": "error", "message": "No text provided"}), 400

if __name__ == "__main__":
    init_db()