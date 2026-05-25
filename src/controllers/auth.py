from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Uporabnik, Stranka, Frizer
import controllers.stranka_opomnik as opomnik_controller
import controllers.opomnik_rezervacij_controller as frizer_opomnik_controller

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
        password_confirm = request.form.get('password_confirm', '')
        vloga    = request.form.get('vloga', 'stranka')
        ime      = request.form.get('ime', '').strip()
        priimek  = request.form.get('priimek', '').strip()
        mail     = request.form.get('mail', '').strip()
        telefon  = request.form.get('telefon', '').strip()

        # ── Validation ────────────────────────────────────────────────────────
        if not username:
            flash("Uporabniško ime ne sme biti prazno.", "error")
            return render_template('register.html')

        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f"Geslo mora imeti vsaj {MIN_PASSWORD_LENGTH} znakov.", "error")
            return render_template('register.html')

        if password != password_confirm:
            flash("Gesli se ne ujemata.", "error")
            return render_template('register.html')

        if vloga == 'stranka' and not priimek:
            flash("Priimek je obvezen za stranke.", "error")
            return render_template('register.html')

        if vloga not in ('stranka', 'frizer'):
            flash("Neveljavna vloga.", "error")
            return render_template('register.html')

        db_session = db.get_session()
        try:
            # Check username is unique
            existing = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()

            if existing:
                flash("Uporabnik s tem imenom že obstaja.", "error")
                return render_template('register.html')

            # Create the user account
            novi_user = Uporabnik(
                username=username,
                password=generate_password_hash(password),
                vloga=vloga
            )
            db_session.add(novi_user)
            db_session.flush()  # populates novi_user.id before commit

            # Create linked stranka or frizer row
            if vloga == 'stranka':
                db_session.add(Stranka(
                    ime=ime or None,
                    priimek=priimek,
                    mail=mail or None,
                    telefon=telefon or None,
                    user_id=novi_user.id
                ))
            elif vloga == 'frizer':
                full_name = f"{ime} {priimek}".strip() or username
                db_session.add(Frizer(
                    ime=full_name,
                    kontakt=mail or telefon or None,
                    user_id=novi_user.id
                ))

            db_session.commit()
            flash("Registracija uspešna! Prijavi se.", "success")

        except Exception as e:
            db_session.rollback()
            import traceback as _tb
            print(f"[REGISTER ERROR] {_tb.format_exc()}", flush=True)
            flash(f"Napaka pri registraciji: {e}", "error")
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

        # Admin shortcut — hardcoded credentials, no DB needed
        if username == 'admin123' and password == 'admin123':
            _clear_rate_limit()
            session["user_id"]  = 0          # sentinel for hardcoded admin
            session["username"] = 'admin123'
            session["role"]     = 'admin'
            flash("Dobrodošel, admin!", "success")
            return redirect('/admin')

        db_session = db.get_session()
        try:
            user = db_session.query(Uporabnik).filter(
                Uporabnik.username == username
            ).first()
        finally:
            db_session.close()

        if user and check_password_hash(user.password, password):
            _clear_rate_limit()
            session["user_id"]  = user.id
            session["username"] = user.username
            session["role"]     = user.vloga
            flash(f"Dobrodošel, {user.username}!", "success")

            if user.vloga == 'admin':
                return redirect('/admin')
            elif user.vloga == 'frizer':
                rezervacije = frizer_opomnik_controller.get_danasnje_rezervacije(user.id)
                if rezervacije:
                    session['opomnik_rezervacije'] = [
                        {
                            'ura': str(r.ura)[:5] if r.ura else '—',
                            'storitev': r.storitev or 'Ni določena',
                            'stranka': r.stranka or '—',
                            'salon': r.salon or '—',
                        }
                        for r in rezervacije
                    ]
                    session['opomnik_tip'] = 'frizer'
                return redirect('/frizer')
            else:
                # Shrani opomnik v session za prikaz na domači strani
                rezervacije = opomnik_controller.get_danasnje_rezervacije(user.id)
                if rezervacije:
                    session['opomnik_rezervacije'] = [
                        {
                            'ura': str(r.ura)[:5] if r.ura else '—',
                            'storitev': r.storitev or 'Ni določena',
                            'frizer': r.frizer or '—',
                            'salon': r.salon or '—',
                        }
                        for r in rezervacije
                    ]
                    session['opomnik_tip'] = 'stranka'
                return redirect('/')

        just_locked   = _record_failed_attempt()
        attempts_left = MAX_LOGIN_ATTEMPTS - session.get('login_attempts', 0)
        if just_locked:
            flash(f"Preveč neuspešnih poskusov. Počakaj {LOCKOUT_SECONDS} sekund.", "error")
        else:
            flash(f"Napačno geslo ali uporabniško ime. Še {attempts_left} poskus(ov) pred zaklepom.", "error")

        return render_template('login.html')

    return render_template("login.html")


def logout():
    session.clear()
    flash("Uspešno si se odjavil.", "success")
    return redirect('/')


def profil():
    if "user_id" not in session:
        return redirect('/login')

    podatki = {}
    user_id = session.get('user_id')
    role = session.get('role')

    # Hardcoded admin (user_id == 0) has no DB row
    if user_id and role in ('stranka', 'frizer'):
        s = db.get_session()
        try:
            if role == 'stranka':
                st = s.query(Stranka).filter(Stranka.user_id == user_id).first()
                if st:
                    podatki = {
                        'ime': st.ime, 'priimek': st.priimek,
                        'mail': st.mail, 'telefon': st.telefon,
                    }
            elif role == 'frizer':
                fr = s.query(Frizer).filter(Frizer.user_id == user_id).first()
                if fr:
                    podatki = {'ime': fr.ime, 'kontakt': fr.kontakt}
        except Exception:
            podatki = {}
        finally:
            s.close()

    return render_template("profil.html", podatki=podatki)