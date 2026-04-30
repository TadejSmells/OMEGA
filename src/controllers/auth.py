from flask import request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Uporabnik

MIN_PASSWORD_LENGTH = 6


def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        vloga = request.form.get('vloga', 'stranka')

        # password length validation
        if len(password) < MIN_PASSWORD_LENGTH:
            return f"Geslo mora imeti vsaj {MIN_PASSWORD_LENGTH} znakov."

        if not username:
            return "Uporabniško ime ne sme biti prazno."

        db_session = db.get_session()
        try:
            existing = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                return "Uporabnik že obstaja!"

            hashed_password = generate_password_hash(password)
            db_session.add(Uporabnik(
                username=username,
                password=hashed_password,
                vloga=vloga
            ))
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()

        return redirect('/login')

    return render_template('register.html')


def login():
    if request.method == "POST":
        username = request.form["username"].strip()
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
            session["role"] = user.vloga

            if user.vloga == 'admin':
                return redirect('/admin')
            elif user.vloga == 'frizer':
                return redirect('/frizer')
            else:
                return redirect('/stranka')

        return "Napačni podatki!"

    return render_template("login.html")


def logout():
    session.clear()
    return redirect('/')


def profil():
    return render_template("profil.html")