from flask import Blueprint, render_template, redirect, url_for, session
import models.model_sprocil as Sporocilo
import db
from models.models import Frizer

def vsa_sporocila():
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

    sporocila = Sporocilo.seznam_sporocil(frizer.id_frizer)
    return render_template('sporocila.html', sporocila=sporocila)

def podrobnosti_sporocila(id):
    sporocilo = Sporocilo.podrobnosti_sporocila(id)
    if sporocilo:
        return render_template('sporocila_tedaili.html', sporocilo=sporocilo)
    else:
        return redirect(url_for('vsa_sporocila'))