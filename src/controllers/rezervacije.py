from flask import render_template, request, redirect
from models import model_rezervacije
from models import model_salon


def nova_rezervacija():
    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')

        rezervacije = model_rezervacije.get_vse_rezervacije()

        for r in rezervacije:
            if str(r[1]) == stranka_id and str(r[2]) == frizer_id:
                return "Ta termin je že rezerviran!"

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
    path = request.args.get('path', '/rezervacije')
    model_rezervacije.izbrisi_rezervacijo(id_rezervacije)
    return redirect(path)

def preklici_rezervacijo(id_rezervacije):
    path = request.args.get('path', '/rezervacije')
    model_rezervacije.preklic_rezervacije(id_rezervacije)
    return redirect(path)

def admin():
    return render_template(
        "rezervacije_admin.html",
        rezervacije=model_rezervacije.get_vse_rezervacije()
    )