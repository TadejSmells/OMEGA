from flask import render_template, session, redirect, flash
from models import model_priljubljene_storitve


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
        podatki = model_priljubljene_storitve.get_priljubljene_storitve(
            session["user_id"]
        )
        priljubljeni_ids = model_priljubljene_storitve.get_priljubljene_ids(
            session["user_id"]
        )
    except Exception:
        podatki = []
        priljubljeni_ids = set()

    return render_template(
        "priljubljene_storitve.html",
        podatki=podatki,
        priljubljeni_ids=priljubljeni_ids,
    )