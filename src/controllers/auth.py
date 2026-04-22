from flask import request, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Uporabnik

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session = db.get_session()
        try:
            existing = session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                return "Uporabnik že obstaja!"

            hashed_password = generate_password_hash(password)
            session.add(Uporabnik(username=username, password=hashed_password))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return redirect('/login')

    return render_template('register.html')


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        session = db.get_session()
        try:
            user = session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()
        finally:
            session.close()

        if user and check_password_hash(user.password, password):
            return "Prijava uspešna!"

        return "Napačni podatki!"

    return render_template("login.html")


def profil():
    return render_template("profil.html")