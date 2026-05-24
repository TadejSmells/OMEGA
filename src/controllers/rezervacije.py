from flask import render_template, request, redirect, session, flash
from models import model_rezervacije
from models import model_salon
from models import komentar_salona  # has get_stranka_id(user_id)


def nova_rezervacija():
    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')
        datum       = request.form.get('datum')
        ura         = request.form.get('ura')
        next_url    = request.form.get('next') or '/rezervacije'

        # If no stranka picked from the form, use the logged-in customer's own id.
        if not stranka_id and session.get('user_id') and session.get('role') == 'stranka':
            stranka_id = komentar_salona.get_stranka_id(session['user_id'])

        if not datum or not ura:
            flash("Datum in ura sta obvezna!", "error")
            return redirect(next_url)

        if not stranka_id:
            flash("Manjka stranka za rezervacijo.", "error")
            return redirect(next_url)

        if frizer_id and model_rezervacije.je_termin_zaseden(frizer_id, datum, ura):
            flash("Ta termin je že zaseden!", "error")
            return redirect(next_url)

        model_rezervacije.dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id, datum, ura)
        flash("Rezervacija je bila uspešno ustvarjena.", "success")
        return redirect(next_url)

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