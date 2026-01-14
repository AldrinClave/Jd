import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ================= DATABASE CONFIG =================
database_url = os.getenv("MYSQL_URL")

# Fix Railway mysql:// → mysql+pymysql://
if database_url and database_url.startswith("mysql://"):
    database_url = database_url.replace(
        "mysql://", "mysql+pymysql://", 1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODEL =================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    ingame_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# ================= AUTO CREATE TABLE =================
with app.app_context():
    db.create_all()

# ================= ROUTES =================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_user = User(
            username=request.form.get("username"),
            ingame_name=request.form.get("ingame_name"),
            password=request.form.get("password")
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("registration.html")

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
