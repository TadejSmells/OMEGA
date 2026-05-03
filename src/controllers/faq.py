import sys
import os
from flask import render_template
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from models import model_faq

def faq():
    return render_template(
        'faq.html',
        faqi=model_faq.pridobi_faq()
    ) 