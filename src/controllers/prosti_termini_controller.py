from flask import render_template, abort
from models import model_salon, model_prosti_termini


def prikazi_termine_za_salon(salon_id):
    """Koledar prostih terminov za gosta — pregled za izbrani salon."""
    try:
        salon = next((s for s in model_salon.get_vse('salon') if s[0] == salon_id), None)
    except Exception:
        salon = None

    if salon is None:
        abort(404)

    try:
        dnevi = model_prosti_termini.get_prosti_termini_po_dnevih(salon_id, dni_naprej=14)
    except Exception:
        dnevi = []

    najhitrejsi_index = model_prosti_termini.najdi_najhitrejsi_index(dnevi)

    return render_template(
        "salon_termini.html",
        salon=salon,
        dnevi=dnevi,
        najhitrejsi_index=najhitrejsi_index,
    )