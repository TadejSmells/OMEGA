from flask import render_template
from models import saloni_model


def saloni():
    saloni_list = []

    try:
        saloni_list = saloni_model.get_saloni()
    except Exception:
        saloni_list = []

    rezultat = []

    for salon in saloni_list:
        salon_id = salon[0]

        try:
            storitve = saloni_model.get_storitve_za_salon(salon_id)
        except Exception:
            storitve = []

        rezultat.append({
            "salon": salon,
            "storitve": storitve
        })

    return render_template(
        "seznam_salonov.html",
        saloni=rezultat
    )