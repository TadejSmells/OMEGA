from flask import render_template, session, redirect, flash
from models import model_prikaz_priljubljenih_storitev


def prikazi():
    """
    Prikaz seznama priljubljenih storitev prijavljene stranke.
    GET /storitve/priljubljene
    """
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "stranka":
        flash("Samo stranke imajo seznam priljubljenih storitev.", "error")
        return redirect("/storitve")

    try:
        podatki = model_prikaz_priljubljenih_storitev.get_priljubljene_storitve(
            session["user_id"]
        )
        priljubljeni_ids = model_prikaz_priljubljenih_storitev.get_priljubljene_ids(
            session["user_id"]
        )
    except Exception:
        podatki = []
        priljubljeni_ids = set()

    return render_template(
        "prikaz_priljubljenih_storitev.html",
        podatki=podatki,
        priljubljeni_ids=priljubljeni_ids,
    )