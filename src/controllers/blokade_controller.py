from flask import render_template, request, redirect
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import model_salon
from models.model_blokade import get_blokade, dodaj_blokado


def blokade():
    if request.method == "POST":
        frizer_id = request.form.get("frizer_id")
        datum = request.form.get("datum")
        ura_od = request.form.get("ura_od")
        ura_do = request.form.get("ura_do")
        razlog = request.form.get("razlog")

        dodaj_blokado(frizer_id, datum, ura_od, ura_do, razlog)
        return redirect("/blokade")

    blokade = get_blokade()

    return render_template(
        "blokade.html",
        blokade=blokade,
        frizerji=model_salon.get_vse('frizer')
    )
