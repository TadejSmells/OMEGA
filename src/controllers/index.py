import logging
from flask import render_template
from models import model_salon

logger = logging.getLogger(__name__)

def home():
    try:
        saloni = model_salon.get_vse('salon')
        storitve = model_salon.get_vse('storitev')
    except Exception:
        logger.error("Napaka pri nalaganju strani.", exc_info=True)
        saloni = []
        storitve = []
    return render_template("zacetna_stran.html", saloni=saloni, storitve=storitve)