"""
controllers/priljubljeni_saloni.py

Zakaj obstaja ta datoteka:
    Upravlja s HTTP zahtevami za priljubljene salone.
    toggle_favorite() se pokliče ko uporabnik klikne zvezdico na salon kartici.
    prikazi() prikaže stran z vsemi priljubljenimi saloni prijavljenega uporabnika.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import request, redirect, url_for, session as flask_session, render_template
from models import model_priljubljeni
from models.models import Stranka
import db


def toggle_favorite(salon_id):
    """
    Preklopi priljubljenost salona za prijavljenega uporabnika.
    Neprijavljen uporabnik je preusmerjen na /login.
    Po operaciji se vrne na stran od koder je prišel (referrer).
    """
    user_id = flask_session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    id_stranke = model_priljubljeni.get_id_stranke(user_id)
    if not id_stranke:
        return redirect(url_for("login"))

    model_priljubljeni.toggle_priljubljenega(id_stranke, salon_id)
    return redirect(request.referrer or url_for("saloni"))


def prikazi():
    """
    Prikaže stran z vsemi priljubljenimi saloni prijavljenega uporabnika.
    """
    user_id = flask_session.get("user_id")
    saloni = model_priljubljeni.get_priljubljene_salone(user_id)
    priljubljeni_ids = model_priljubljeni.get_priljubljene_ids(user_id)
    return render_template(
        "priljubljeni_saloni.html",
        saloni=saloni,
        priljubljeni_ids=priljubljeni_ids
    )
