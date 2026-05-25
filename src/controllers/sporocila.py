from flask import render_template, redirect, url_for, session

import db
from models.models import Frizer
import models.model_sprocil as model_sprocil


def vsa_sporocila():
    """Prikaže vsa sporočila prijavljenega frizerja."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    s = db.get_session()
    try:
        frizer = s.query(Frizer).filter(Frizer.user_id == user_id).first()
    finally:
        s.close()

    if not frizer:
        return redirect(url_for('login'))

    sporocila = model_sprocil.seznam_sporocil(frizer.id_frizer)
    return render_template('sporocila.html', sporocila=sporocila)


def podrobnosti_sporocila(id):
    """Prikaže podrobnosti enega sporočila."""
    sporocilo = model_sprocil.podrobnosti_sporocila(id)
    if sporocilo:
        return render_template('sporocila_tedaili.html', sporocilo=sporocilo)
    return redirect(url_for('vsa_sporocila'))
