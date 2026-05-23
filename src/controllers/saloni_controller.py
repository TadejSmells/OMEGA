"""
controllers/saloni_controller.py

Zakaj obstaja ta datoteka:
    Prikaže seznam vseh salonov z njihovimi storitvami.
    Pošlje tudi priljubljeni_ids v template da se zvezdica
    obarva pravilno za vsakega prijavljenega uporabnika.
"""

from flask import render_template, session
from models import model_salon
from models import model_priljubljeni


def saloni():
    """
    Pridobi vse salone z optimizirano JOIN poizvedbo (brez N+1 problema)
    ter id-je priljubljenih salonov za prijavljenega uporabnika.
    Priljubljeni saloni so prikazani na začetku seznama.
    """
    user_id = session.get("user_id")
    priljubljeni_ids = model_priljubljeni.get_priljubljene_ids(user_id)

    try:
        # Pass favourites to the model so it can sort them to the front
        rezultat = model_salon.get_saloni_s_storitvami(priljubljeni_ids)
    except Exception:
        rezultat = []

    return render_template(
        "seznam_salonov.html",
        saloni=rezultat,
        priljubljeni_ids=priljubljeni_ids
    )