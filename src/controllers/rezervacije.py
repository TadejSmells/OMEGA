from flask import render_template, request, redirect
from models import model_rezervacije
from models import model_salon


def nova_rezervacija():
    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')

        model_rezervacije.dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id)
        return redirect('/rezervacije')

    return render_template(
        "salon_rezervacija.html",
        stranke=model_salon.get_vse('stranka'),
        frizerji=model_salon.get_vse('frizer'),
        saloni=model_salon.get_vse('salon'),
        storitve=model_salon.get_vse('storitev'),
        rezervacije=model_rezervacije.get_vse_rezervacije()
    )


def izbrisi_rezervacijo(id_rezervacije):
    model_rezervacije.izbrisi_rezervacijo(id_rezervacije)
    return redirect('/rezervacije')