from flask import render_template, session, redirect
from models import model_cenikstoritev


def pridobi_storitve():
    try:
        podatki = model_cenikstoritev.get_vse_storitve()
    except Exception:
        podatki = []

    return render_template(
        "seznam_storitev.html",
        podatki=podatki
    )


def stranka():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "stranka":
        return "Nimaš dostopa"
    return "Stranka panel"