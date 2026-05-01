from flask import render_template, request, redirect
from models import model_uredi_rezervacijo
from models import model_salon


def uredi_rezervacijo(id_rezervacije):
    rezervacija = model_uredi_rezervacijo.get_rezervacijo(id_rezervacije)

    if rezervacija is None:
        return "Rezervacija ne obstaja!", 404

    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')

        model_uredi_rezervacijo.uredi_rezervacijo(
            id_rezervacije, stranka_id, frizer_id, salon_id, storitev_id
        )
        return redirect('/rezervacije')

    return render_template(
        "uredi_rezervacijo.html",
        rezervacija=rezervacija,
        stranke=model_salon.get_vse('stranka'),
        frizerji=model_salon.get_vse('frizer'),
        saloni=model_salon.get_vse('salon'),
        storitve=model_salon.get_vse('storitev'),
    )
