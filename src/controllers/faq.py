from flask import render_template
from models import model_faq


def faq():
    return render_template(
        'faq.html',
        faqi=model_faq.pridobi_faq()
    )