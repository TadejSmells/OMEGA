from flask import render_template, session, redirect, request
from werkzeug.security import generate_password_hash
import models.model_salon as model_salon
import models.model_rezervacije as model_rezervacije
import db
from models.models import Uporabnik
from datetime import date, timedelta


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

    vse = model_rezervacije.get_vse_rezervacije()

    danes = date.today()
    zacetek_tedna = danes - timedelta(days=danes.weekday())
    konec_tedna = zacetek_tedna + timedelta(days=6)

    rezervacije_teden = []
    for r in vse:
        try:
            datum_r = date.fromisoformat(str(r[5]))
            if zacetek_tedna <= datum_r <= konec_tedna:
                rezervacije_teden.append({
                    "stranka_ime":  r[1] or "—",
                    "frizer_ime":   r[2] or "—",
                    "storitev_ime": r[4] or "—",
                    "datum":        str(r[5]) or "—",
                    "ura":          str(r[6]) or "—",
                    "status":       r[8] or "—",
                })
        except:
            pass

    # Zadnja aktivnost - zadnjih 5 rezervacij
    zadnja_aktivnost = []
    for r in vse[:5]:
        if r[8] == 'cancelled':
            tip = "Rezervacija preklicana"
            dot = "rose"
        else:
            tip = "Nova rezervacija"
            dot = "brown"
        zadnja_aktivnost.append({
            "tip":    tip,
            "ime":    r[1] or "—",
            "datum":  str(r[5]) or "—",
            "ura":    str(r[6]) or "—",
            "dot":    dot,
        })

    danes_str = str(danes)
    stats = {
        "rezervacije_teden": len(rezervacije_teden),
        "rezervacije_danes":  sum(1 for r in vse if str(r[5]) == danes_str),
        "aktivne_stranke":    len(model_salon.get_vse('stranka')),
        "promet_teden": f"{sum(float(r[7]) for r in vse if r[7] and r[8] == 'active' and zacetek_tedna <= date.fromisoformat(str(r[5])) <= konec_tedna):.2f}",
        "prosti_termini":     "—",
    }

    return render_template(
        "admin.html",
        stats=stats,
        rezervacije_teden=rezervacije_teden,
        zadnja_aktivnost=zadnja_aktivnost,
    )


def frizer():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("frizer", "admin"):
        return "Nimaš dostopa.", 403
    return render_template("frizer.html")