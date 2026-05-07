from flask import render_template, request
from models import model_kontakt_stranka


def seznam_kontaktov():
    kontakti = model_kontakt_stranka.get_vse_kontakti()

    izbrana_id = request.args.get('stranka_id', type=int)
    stranka = None
    if izbrana_id:
        stranka = model_kontakt_stranka.get_stranka(izbrana_id)

    return render_template(
        "seznam_kontaktov.html",
        kontakti=kontakti,
        stranka=stranka,
        izbrana_id=izbrana_id,
    )

