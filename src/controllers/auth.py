from flask import Blueprint, request, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from db import get_conaction

auth = Blueprint("auth", __name__)

# REGISTRACIJA
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_conaction()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Uporabnik že obstaja!"
        
        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# PRIJAVA
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return "Prijava uspešna!"

        return "Napačni podatki!"

    return render_template("login.html")