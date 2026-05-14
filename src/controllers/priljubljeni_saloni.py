import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import request, redirect, url_for, session as flask_session
from models import priljubljeni_saloni as priljubljeni_model
from models.models import Stranka
import db

def toggle_favorite(salon_id):
    user_id = flask_session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    db_session = db.get_session()
    try:
        stranka = db_session.query(Stranka)\
            .filter(Stranka.user_id == user_id)\
            .first()
        if not stranka:
            return redirect(url_for("login"))
        id_stranke = stranka.id_stranke
    finally:
        db_session.close()

    priljubljeni_model.toggle_priljubljenega(id_stranke, salon_id)
    return redirect(request.referrer or url_for("saloni"))