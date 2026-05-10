from flask import render_template, abort
from models import model_frizer


def frizer_profil(frizer_id):
    """Prikaže osebno stran posameznega frizerja."""
    frizer = model_frizer.get_frizer(frizer_id)

    if frizer is None:
        abort(404)

    salon = model_frizer.get_salon_frizerja(frizer_id)
    storitve = model_frizer.get_storitve_frizerja(frizer_id)

    return render_template(
        "frizer_profil.html",
        frizer=frizer,
        salon=salon,
        storitve=storitve
    )


def seznam_frizerjev():
    """Prikaže seznam vseh frizerjev."""
    frizerji = model_frizer.get_vsi_frizerji()

    return render_template(
        "seznam_frizerjev.html",
        frizerji=frizerji
    )