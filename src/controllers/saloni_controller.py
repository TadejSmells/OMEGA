from flask import render_template
from models import model_salon


def saloni():
    try:
        # uses optimised single query instead of N+1
        rezultat = model_salon.get_saloni_s_storitvami()
    except Exception:
        rezultat = []

    return render_template(
        "seznam_salonov.html",
        saloni=rezultat
    )