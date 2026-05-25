from flask import render_template, session, redirect
from models import model_kontakt_stranka


def kontakti_mojih_strank():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "frizer":
        return redirect("/")

    user_id = session["user_id"]

    stranke = model_kontakt_stranka.get_stranke_frizerja(user_id)

    return render_template(
        "seznam_kontaktov.html",
        stranke=stranke
    )


def kontakt_posamezne_stranke(id_stranke):
    """Podroben kontakt ene stranke — samo za prijavljenega frizerja."""
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "frizer":
        return redirect("/")

    user_id = session["user_id"]

    # Stranka mora biti med strankami tega frizerja (varnost).
    moje = model_kontakt_stranka.get_stranke_frizerja(user_id)
    dovoljeni = {s.id_stranke for s in moje}

    stranka = None
    if id_stranke in dovoljeni:
        stranka = model_kontakt_stranka.get_stranka(id_stranke)

    return render_template(
        "kontakt_stranka.html",
        stranka=stranka
    )

