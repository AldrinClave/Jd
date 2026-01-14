from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ================= DATABASE =================
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ingame_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

# ================= ROUTES =================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        ingame_name = request.form["ingame_name"]
        password = request.form["password"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (username, ingame_name, password) VALUES (?, ?, ?)",
            (username, ingame_name, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("registration.html")

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)
