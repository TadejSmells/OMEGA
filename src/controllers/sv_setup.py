from flask import render_template, session, redirect
import models.model_salon as model_salon


def setup_db():
    success = model_salon.setup_db()
    tables = {
        "salon": success,
        "frizer": success,
        "stranka": success,
        "storitev": success,
        "urnik": success,
        "rezervacija": success
    }
    return render_template("sv_setup.html", tables=tables)

def polni_db():
    success = model_salon.polni_db()
    tabless={
        "salon": success,
        "frizer": success,
        "stranka": success,
        "storitev": success,
        "urnik": success,
        "rezervacija": success
    }
    return render_template("sv_setup.html", tables=tabless)
    

def admin():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return "Nimaš dostopa"

    return "Admin panel"