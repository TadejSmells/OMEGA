from flask import render_template, request, redirect
from models import model_salon


def pregled():
    """Preusmeri na glavni seznam salonov."""
    return redirect('/saloni')


def urnik():
    if request.method == 'POST':
        model_salon.dodaj_urnik(
            request.form.get('frizer_id'),
            request.form.get('dan'),
            request.form.get('ura')
        )
        return redirect('/urnik')
    return render_template(
        "urnik.html",
        urnik=model_salon.get_vse('urnik'),
        frizerji=model_salon.get_vse('frizer')
    )


def zgodovina():
    rezervacije = model_salon.get_vse('rezervacija')
    return render_template("zgodovina.html", rezervacije=rezervacije)


def prosti_termini():
    salon_id = request.args.get('salon_id', type=int)
    saloni = model_salon.get_vse('salon')

    if not salon_id:
        return render_template("prosti_termini.html", saloni=saloni,
                               salon=None, dnevi=[], najhitrejsi_index=None)

    salon = next((s for s in saloni if s[0] == salon_id), None)
    if salon is None:
        return render_template("prosti_termini.html", saloni=saloni,
                               salon=None, dnevi=[], najhitrejsi_index=None)

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
