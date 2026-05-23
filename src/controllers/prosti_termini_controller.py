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
        dnevi = model_prosti_termini.get_prosti_termini_po_dnevih(salon_id, dni_naprej=7)
    except Exception:
        dnevi = []

    najhitrejsi_index = model_prosti_termini.najdi_najhitrejsi_index(dnevi)

    return render_template(
        "salon_termini.html",
        salon=salon,
        dnevi=dnevi,
        najhitrejsi_index=najhitrejsi_index,
    )

def prosti_termini():
    salon_id = request.args.get('salon_id', type=int)

    saloni = model_salon.get_vse('salon')  # [(id, ime, naslov, mesto, tel), ...]

    if not salon_id:
        return render_template("prosti_termini.html", saloni=saloni, salon=None, dnevi=[], najhitrejsi_index=None)

    # poišči izbrani salon
    salon = next((s for s in saloni if s[0] == salon_id), None)
    if salon is None:
        return render_template("prosti_termini.html", saloni=saloni, salon=None, dnevi=[], najhitrejsi_index=None)

    from models import model_prosti_termini
    dnevi = model_prosti_termini.get_prosti_termini_po_dnevih(salon_id)
    najhitrejsi_index = model_prosti_termini.najdi_najhitrejsi_index(dnevi)

    return render_template(
        "prosti_termini.html",
        saloni=saloni,
        salon=salon,
        dnevi=dnevi,
        najhitrejsi_index=najhitrejsi_index,
    )