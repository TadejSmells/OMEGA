import logging
from flask import render_template
from models import model_salon

logger = logging.getLogger(__name__)


def saloni():
    try:
        rezultat = model_salon.get_saloni_s_storitvami()
    except Exception:
        logger.error("Napaka pri nalaganju salonov.", exc_info=True)
        rezultat = []

    return render_template(
        "seznam_salonov.html",
        saloni=rezultat
    )