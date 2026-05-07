from flask import render_template, session, redirect
from werkzeug.security import generate_password_hash
import models.model_salon as model_salon
import db
from models.models import Uporabnik


def _ensure_admin():
    """Insert the hardcoded admin into the DB if it doesn't exist yet."""
    s = db.get_session()
    try:
        if not s.query(Uporabnik).filter_by(username='admin123').first():
            s.add(Uporabnik(
                username='admin123',
                password=generate_password_hash('admin123'),
                vloga='admin'
            ))
            s.commit()
    except Exception:
        s.rollback()
    finally:
        s.close()


def setup_db():
    success = model_salon.setup_db()
    _ensure_admin()
    tables = {
        "salon":      success,
        "frizer":     success,
        "stranka":    success,
        "storitev":   success,
        "urnik":      success,
        "rezervacija": success,
        "users":      success,
    }
    return render_template("sv_setup.html", tables=tables)


def polni_db():
    success = model_salon.polni_db()
    tables = {
        "salon":      success,
        "frizer":     success,
        "stranka":    success,
        "storitev":   success,
        "urnik":      success,
        "rezervacija": success,
        "users":      success,
    }
    return render_template("sv_setup.html", tables=tables)


def admin():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403
    return render_template("admin.html")


def frizer():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("frizer", "admin"):
        return "Nimaš dostopa.", 403
    return render_template("frizer.html")