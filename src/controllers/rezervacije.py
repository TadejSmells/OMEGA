from flask import render_template, request, redirect, flash
from models import model_rezervacije
from models import model_salon


def nova_rezervacija():
    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')
        datum       = request.form.get('datum')
        ura         = request.form.get('ura')
        next_url    = request.form.get('next', '/rezervacije')

        if not datum or not ura:
            flash("Datum in ura sta obvezna.", "error")
            return redirect(next_url)

        if not stranka_id:
            flash("Za rezervacijo se moraš prijaviti kot stranka.", "error")
            return redirect(next_url)

        # Preveri, ali je termin pri tem frizerju že zaseden
        if model_rezervacije.je_termin_zaseden(frizer_id, datum, ura):
            flash("Ta termin je že zaseden. Izberi drug termin.", "error")
            return redirect(next_url)

        model_rezervacije.dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id, datum, ura)
        flash("Rezervacija je bila uspešno poslana!", "success")
        return redirect(next_url)

    return render_template(
        "salon_rezervacija.html",
        stranke=model_salon.get_vse('stranka'),
        frizerji=model_salon.get_vse('frizer'),
        saloni=model_salon.get_vse('salon'),
        storitve=model_salon.get_vse('storitev'),
        rezervacije=model_rezervacije.get_vse_rezervacije(),
        pre={},
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