from flask import render_template
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