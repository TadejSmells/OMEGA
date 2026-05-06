from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Uporabnik

MIN_PASSWORD_LENGTH = 6
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 60


def _check_rate_limit():
    now = time.time()
    lockout_until = session.get('login_lockout_until', 0)
    if lockout_until and now < lockout_until:
        return True, int(lockout_until - now)
    if lockout_until and now >= lockout_until:
        session.pop('login_attempts', None)
        session.pop('login_lockout_until', None)
    return False, 0


def _record_failed_attempt():
    attempts = session.get('login_attempts', 0) + 1
    session['login_attempts'] = attempts
    session.modified = True
    if attempts >= MAX_LOGIN_ATTEMPTS:
        session['login_lockout_until'] = time.time() + LOCKOUT_SECONDS
        session.modified = True
        return True
    return False


def _clear_rate_limit():
    session.pop('login_attempts', None)
    session.pop('login_lockout_until', None)
    session.modified = True


def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        vloga = request.form.get('vloga', 'stranka')

        if not username:
            flash("Uporabniško ime ne sme biti prazno.", "error")
            return render_template('register.html')

        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f"Geslo mora imeti vsaj {MIN_PASSWORD_LENGTH} znakov.", "error")
            return render_template('register.html')

        db_session = db.get_session()
        try:
            existing = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                flash("Uporabnik s tem imenom že obstaja.", "error")
                return render_template('register.html')

            db_session.add(Uporabnik(
                username=username,
                password=generate_password_hash(password),
                vloga=vloga
            ))
            db_session.commit()
            flash("Registracija uspešna! Prijavi se.", "success")
        except:
            db_session.rollback()
            flash("Napaka pri registraciji. Poskusi znova.", "error")
            return render_template('register.html')
        finally:
            db_session.close()

        return redirect('/login')

    return render_template('register.html')


def login():
    if request.method == "POST":
        locked, remaining = _check_rate_limit()
        if locked:
            flash(f"Preveč neuspešnih poskusov. Počakaj {remaining} sekund.", "error")
            return render_template('login.html')

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
            _clear_rate_limit()
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

        just_locked = _record_failed_attempt()
        attempts_left = MAX_LOGIN_ATTEMPTS - session.get('login_attempts', 0)
        if just_locked:
            flash(f"Preveč neuspešnih poskusov. Počakaj {LOCKOUT_SECONDS} sekund.", "error")
        else:
            flash(f"Napačno geslo. Še {attempts_left} poskus(ov) pred zaklepom.", "error")

        return render_template('login.html')

    return render_template("login.html")


def logout():
    session.clear()
    flash("Uspešno si se odjavil.", "success")
    return redirect('/')


def profil():
    if "user_id" not in session:
        return redirect('/login')
    return render_template("profil.html")