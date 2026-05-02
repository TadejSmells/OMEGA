import logging
from flask import render_template, session, redirect
from models import model_cenikstoritev
from models import model_rezervacije

logger = logging.getLogger(__name__)


def pridobi_storitve():
    try:
        podatki = model_cenikstoritev.get_vse_storitve()
    except Exception:
        logger.error("Napaka pri nalaganju storitev.", exc_info=True)
        podatki = []
    return render_template("seznam_storitev.html", podatki=podatki)


def stranka():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("stranka", "admin"):
        return "Nimaš dostopa.", 403

    user_id = session.get("user_id")
    try:
        rezervacije = model_rezervacije.get_rezervacije_za_uporabnika(user_id)
    except Exception:
        logger.error(f"Napaka pri nalaganju rezervacij za uporabnika {user_id}.", exc_info=True)
        rezervacije = []

    return render_template("stranka_panel.html", rezervacije=rezervacije)