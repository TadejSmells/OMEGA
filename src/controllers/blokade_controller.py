from flask import render_template, request, redirect
from datetime import date, timedelta
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import model_salon
from models.model_blokade import get_blokade, dodaj_blokado


def blokade():
    if request.method == "POST":
        frizer_id = request.form.get("frizer_id")
        razlog = request.form.get("razlog")

        datum_od = date.fromisoformat(request.form.get("datum_od"))
        datum_do = date.fromisoformat(request.form.get("datum_do"))

        d = datum_od
        while d <= datum_do:
            dodaj_blokado(frizer_id, d.isoformat(), "00:00", "23:59", razlog)
            d += timedelta(days=1)

        return redirect("/blokade")

    blokade = get_blokade()

    return render_template(
        "blokade.html",
        blokade=blokade,
        frizerji=model_salon.get_vse('frizer')
    )