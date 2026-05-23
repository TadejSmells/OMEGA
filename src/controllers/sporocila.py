from flask import Blueprint, render_template, request, redirect, url_for, session

import db
from models.models import Frizer
import models.model_sprocil as model_sprocil
import models.model_frizer as model_frizer
import models.model_sprocil as Sporocilo


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
    
def kontakt_frizer():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        stranka_id = session["user_id"]
        frizer_id = request.form.get("frizer_id")
        vsebina = request.form.get("vsebina")

        model_sprocil.poslji_sporocilo(
            stranka_id,
            frizer_id,
            vsebina
        )

        return redirect("/sporocila?success=1")

    frizerji = model_frizer.get_vsi_frizerji()

    return render_template("sporocila.html", frizerji=frizerji)


def moja_sporocila():

    if "user_id" not in session:
        return redirect("/login")

    frizer_id = session["user_id"]

    sporocila = model_sprocil.get_sporocila_frizerja(frizer_id)

    return render_template(
        "sporocila_inbox.html",
        sporocila=sporocila
    )

def sporocilo_detail(id):

    sporocilo = model_sporocil.podrobnosti_sporocila(id)

    return render_template("sporocilo_detail.html", sporocilo=sporocilo)