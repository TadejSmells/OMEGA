from flask import render_template, session
from models import model_salon
from models import model_rezervacije_stranke


def home():
    try:
        saloni = model_salon.get_vse('salon')
        storitve = model_salon.get_vse('storitev')
    except Exception:
        saloni = []
        storitve = []

    preklicane_rezervacije = []

    if session.get("user_id") and session.get("role") == "stranka":
        try:
            preklicane_rezervacije = model_rezervacije_stranke.get_preklicane_rezervacije_uporabnika(
                session["user_id"]
            )
        except Exception:
            preklicane_rezervacije = []

    return render_template(
        "zacetna_stran.html",
        saloni=saloni,
        storitve=storitve,
        preklicane_rezervacije=preklicane_rezervacije
    )