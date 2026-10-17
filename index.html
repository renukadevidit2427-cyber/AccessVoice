
from flask import Flask, request, jsonify, send_file
import sqlite3
app = Flask(__name__)
DATABASE = "accessvoice.db"
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


# Display the website
@app.route("/")
def home():
    return send_file("index.html")


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

    connection.execute(
        "INSERT INTO messages (message) VALUES (?)",
        (message,)
    )

    connection.commit()
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

    rows = connection.execute(
        """
        SELECT id, message, created_at
        FROM messages
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify({
        "status": "success",
        "messages": [dict(row) for row in rows]
    })


# Delete one message using its database ID
@app.route("/api/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    connection = get_db_connection()

    cursor = connection.execute(
        "DELETE FROM messages WHERE id = ?",
        (message_id,)
    )

    connection.commit()
    deleted_count = cursor.rowcount
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


# Start the application
if __name__ == "__main__":
    create_table()
    app.run(debug=True)
