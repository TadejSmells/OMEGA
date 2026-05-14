from flask import render_template, session as flask_session
from models import saloni_model
from models import priljubljeni_saloni as priljubljeni_model
from models.models import Stranka
import db

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

    priljubljeni_ids = []
    user_id = flask_session.get("user_id")
    if user_id:
        db_session = db.get_session()
        try:
            stranka = db_session.query(Stranka)\
                .filter(Stranka.user_id == user_id)\
                .first()
            if stranka:
                priljubljeni_ids = priljubljeni_model.get_priljubljeni(stranka.id_stranke)
        finally:
            db_session.close()

    return render_template(
        "seznam_salonov.html",
        saloni=rezultat,
        priljubljeni_ids=priljubljeni_ids
    )