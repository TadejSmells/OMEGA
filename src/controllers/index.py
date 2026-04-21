from flask import render_template
from models import model_salon

def home():
    try:
        saloni = model_salon.get_vse('salon')
        storitve = model_salon.get_vse('storitev')
    except Exception:
        saloni = []
        storitve = []
    return render_template("zacetna_stran.html", saloni=saloni, storitve=storitve)
