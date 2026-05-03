from flask import request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import db
from models.models import Uporabnik


def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_session = db.get_session()
        try:
            existing = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                return "Uporabnik že obstaja!"

            hashed_password = generate_password_hash(password)
            db_session.add(Uporabnik(username=username, password=hashed_password))
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()

        return redirect('/login')

    return render_template('register.html')


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db_session = db.get_session()
        try:
            user = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()
        finally:
            db_session.close()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect('/profil')

        return "Napačni podatki!"

    return render_template("login.html")


def profil():
    if "user_id" not in session:
        return redirect('/login')
    return render_template("profil.html")