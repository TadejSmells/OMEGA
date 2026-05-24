"""
controllers/priljubljeni_saloni.py

toggle_favorite() — called when user clicks the star on a salon card.
prikazi()         — shows the /priljubljeni_saloni page.

All roles (stranka, frizer, admin) can favourite salons.
Unauthenticated visitors are redirected to /login.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import request, redirect, url_for, session as flask_session, render_template
from models import model_priljubljeni


def toggle_favorite(salon_id):
    user_id = flask_session.get("user_id")
    if not user_id:
        # Not logged in — redirect to login
        return redirect(url_for("login"))

    # _get_fav_key works for all roles; no longer blocks frizerji/admins
    fav_key = model_priljubljeni._get_fav_key(user_id)
    model_priljubljeni.toggle_priljubljenega(fav_key, salon_id)
    return redirect(request.referrer or url_for("saloni"))


def prikazi():
    user_id = flask_session.get("user_id")
    saloni = model_priljubljeni.get_priljubljene_salone(user_id)
    priljubljeni_ids = model_priljubljeni.get_priljubljene_ids(user_id)
    return render_template(
        "priljubljeni_saloni.html",
        saloni=saloni,
        priljubljeni_ids=priljubljeni_ids
    )