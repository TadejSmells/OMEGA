from flask import render_template, session, redirect
import models.model_salon as model_salon
from models import model_rezervacije


def setup_db():
    success = model_salon.setup_db()
    tables = {
        "salon": success, "frizer": success, "stranka": success,
        "storitev": success, "urnik": success, "rezervacija": success,
        "users": success, "faq": success
    }
    return render_template("sv_setup.html", tables=tables)


def polni_db():
    success = model_salon.polni_db()
    tables = {
        "salon": success, "frizer": success, "stranka": success,
        "storitev": success, "urnik": success, "rezervacija": success,
        "users": success, "faq": success
    }
    return render_template("sv_setup.html", tables=tables)


def admin():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    rezervacije = model_rezervacije.get_vse_rezervacije()

    stats = {
        'saloni':      len(model_salon.get_salone()),
        'frizerji':    len(model_salon.get_frizerje()),
        'stranke':     len(model_salon.get_stranke()),
        'rezervacije': len(rezervacije),
    }

    return render_template("admin.html", stats=stats, rezervacije=rezervacije)