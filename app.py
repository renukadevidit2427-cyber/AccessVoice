
from flask import Flask, request, jsonify, send_file
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "accessvoice.db")


# Connect to the SQLite database
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Create the messages table
def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# Create the table when the application starts
create_table()


# Display the website
@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "index.html"))


# Check whether the backend is running
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "AccessVoice backend is running!"
    })


# Save a new message
@app.route("/api/message", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "status": "error",
            "message": "Message must be text."
        }), 400

    message = message.strip()

    if not message:
        return jsonify({
            "status": "error",
            "message": "Please enter a message."
        }), 400

    if len(message) > 500:
        return jsonify({
            "status": "error",
            "message": "Message must be 500 characters or less."
        }), 400

    connection = get_db_connection()

    try:
        connection.execute(
            "INSERT INTO messages (message) VALUES (?)",
            (message,)
        )
        connection.commit()
    finally:
        connection.close()

    return jsonify({
        "status": "success",
        "message": "Message saved successfully!",
        "user_message": message
    })


# Get all saved messages
@app.route("/api/messages", methods=["GET"])
def get_messages():
    connection = get_db_connection()

    try:
        rows = connection.execute("""
            SELECT id, message, created_at
            FROM messages
            ORDER BY id DESC
        """).fetchall()

        messages = [dict(row) for row in rows]
    finally:
        connection.close()

    return jsonify({
        "status": "success",
        "messages": messages
    })


# Delete one message using its database ID
@app.route(
    "/api/messages/<int:message_id>",
    methods=["DELETE"]
)
def delete_message(message_id):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM messages WHERE id = ?",
            (message_id,)
        )
        connection.commit()
        deleted_count = cursor.rowcount
    finally:
        connection.close()

    if deleted_count == 0:
        return jsonify({
            "status": "error",
            "message": "Message not found."
        }), 404

    return jsonify({
        "status": "success",
        "message": "Message deleted successfully!"
    })


# Start the application locally
if __name__ == "__main__":
    app.run(debug=True)
