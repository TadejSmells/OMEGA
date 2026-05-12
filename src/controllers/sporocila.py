from flask import Blueprint, render_template, redirect, url_for
from models.model_sporocila import Sporocilo

sporocila_bp = Blueprint("sporocila", __name__)


# Seznam vseh sporočil
def seznam_sporocil():

    sporocila = Sporocilo.query.order_by(
        Sporocilo.datum.desc()
    ).all()

    return render_template(
        "sporocila.html",
        sporocila=sporocila
    )


# Podrobnosti sporočila
def podrobnosti_sporocila(id):

    sporocilo = Sporocilo.query.get_or_404(id)

    # označi kot prebrano
    sporocilo.prebrano = True

    from db import db
    db.session.commit()

    return render_template(
        "sporocilo_detail.html",
        sporocilo=sporocilo
    )