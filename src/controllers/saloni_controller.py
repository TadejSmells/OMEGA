from flask import render_template
from models import model_salon  # fixed: was 'saloni_model' which doesn't exist


def saloni():
    saloni_list = []

    try:
        saloni_list = model_salon.get_vse('salon')
    except Exception:
        saloni_list = []

    rezultat = []

    for salon in saloni_list:
        salon_id = salon[0]

        try:
            storitve = model_salon.get_storitve_za_salon(salon_id)
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