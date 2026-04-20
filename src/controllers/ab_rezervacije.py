from flask import render_template
from models import model_rezervacije


def pregled_rezervacij():
    return render_template(
        "vse_rezervacije.html",
        rezervacije=model_rezervacije.get_vse_rezervacije()
    )