from flask import render_template, request, redirect
from models import model_cenikstoritev


def pridobi_storitve():

    return render_template(
        "cenik_storitev.html",
        podatki = model_cenikstoritev.get_vse_storitve()
    )