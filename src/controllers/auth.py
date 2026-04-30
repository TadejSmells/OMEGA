from flask import request, render_template, redirect, session, flash
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

        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f"Geslo mora imeti vsaj {MIN_PASSWORD_LENGTH} znakov.", "error")
            return redirect('/register')

        if not username:
            flash("Uporabniško ime ne sme biti prazno.", "error")
            return redirect('/register')

        db_session = db.get_session()
        try:
            existing = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                flash("Uporabnik s tem imenom že obstaja.", "error")
                return redirect('/register')

            hashed_password = generate_password_hash(password)
            db_session.add(Uporabnik(
                username=username,
                password=hashed_password,
                vloga=vloga
            ))
            db_session.commit()
            flash("Registracija uspešna! Prijavi se.", "success")
        except:
            db_session.rollback()
            flash("Napaka pri registraciji. Poskusi znova.", "error")
            return redirect('/register')
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
            flash(f"Dobrodošel, {user.username}!", "success")

            if user.vloga == 'admin':
                return redirect('/admin')
            elif user.vloga == 'frizer':
                return redirect('/frizer')
            else:
                return redirect('/')

        flash("Napačno uporabniško ime ali geslo.", "error")
        return redirect('/login')

    return render_template("login.html")


def logout():
    username = session.get("username", "")
    session.clear()
    flash(f"Uspešno si se odjavil.", "success")
    return redirect('/')


def profil():
    return render_template("profil.html")