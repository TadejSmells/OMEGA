from flask import render_template, session, redirect
from models import model_cenikstoritev
from models import model_rezervacije


def pridobi_storitve():
    try:
        podatki = model_cenikstoritev.get_vse_storitve()
    except Exception:
        podatki = []
    return render_template("seznam_storitev.html", podatki=podatki)


def stranka():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("stranka", "admin"):
        return "Nimaš dostopa.", 403

    # get this user's reservations
    user_id = session.get("user_id")
    try:
        rezervacije = model_rezervacije.get_rezervacije_za_uporabnika(user_id)
    except Exception:
        rezervacije = []

    return render_template("stranka_panel.html", rezervacije=rezervacije)
