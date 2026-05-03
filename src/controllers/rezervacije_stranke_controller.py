from flask import render_template, request
from models import model_rezervacije_stranke
 
 
def rezervacije_stranke():
    stranke = model_rezervacije_stranke.get_vse_stranke()
 
    izbrana_id = request.args.get('stranka_id', type=int)
    rezervacije = None
    if izbrana_id:
        rezervacije = model_rezervacije_stranke.get_rezervacije_stranke(izbrana_id)
 
    return render_template(
        "rezervacije_stranke.html",
        stranke=stranke,
        rezervacije=rezervacije,
        izbrana_id=izbrana_id,
    )
