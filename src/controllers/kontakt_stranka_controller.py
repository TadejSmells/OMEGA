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

