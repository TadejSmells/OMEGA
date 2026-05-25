from flask import render_template, abort
from models import model_salon
from models import komentar_salona as ks_model  

def salon_detail(salon_id):
    try:
        salon = next((s for s in model_salon.get_vse('salon') if s[0] == salon_id), None)
    except Exception:
        salon = None

    if salon is None:
        abort(404)

    try:
        storitve = model_salon.get_storitve_za_salon(salon_id)
    except Exception:
        storitve = []

    try:
        komentarji = ks_model.get_komentarji_salona(salon_id)  # ← dodaj
    except Exception:
        komentarji = []

    povprecje = (
        round(sum(k.ocena for k in komentarji) / len(komentarji), 1)
        if komentarji else None
    )

    return render_template(
        "salon.html",
        salon=salon,
        storitve=storitve,
        komentarji=komentarji,   # ← zamenjaj ocene=[]
        povprecje=povprecje,
    )