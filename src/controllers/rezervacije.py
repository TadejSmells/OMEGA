from flask import render_template, request, redirect, flash
from models import model_rezervacije
from models import model_salon


def nova_rezervacija():
    if request.method == 'POST':
        stranka_id  = request.form.get('stranka_id')
        frizer_id   = request.form.get('frizer_id')
        salon_id    = request.form.get('salon_id')
        storitev_id = request.form.get('storitev_id')
        datum       = request.form.get('datum') or None
        ura         = request.form.get('ura') or None

        if not stranka_id or not frizer_id:
            flash("Izberi stranko in frizerja.", "error")
            return redirect('/rezervacije')

        if not datum or not ura:
            flash("Datum in ura sta obvezna.", "error")
            return redirect('/rezervacije')

        try:
            model_rezervacije.dodaj_rezervacijo(
                stranka_id, frizer_id, salon_id, storitev_id, datum, ura
            )
            flash("Rezervacija je bila uspešno dodana!", "success")
            return redirect('/rezervacije')

        except ValueError as e:
            flash(str(e), "error")
            return redirect('/rezervacije')

        except Exception:
            flash("Napaka pri dodajanju rezervacije. Poskusi znova.", "error")
            return redirect('/rezervacije')

    return render_template(
        "salon_rezervacija.html",
        stranke=model_salon.get_stranke(),
        frizerji=model_salon.get_frizerje(),
        saloni=model_salon.get_salone(),
        storitve=model_salon.get_storitve(),
        rezervacije=model_rezervacije.get_vse_rezervacije()
    )


def izbrisi_rezervacijo(id_rezervacije):
    try:
        model_rezervacije.izbrisi_rezervacijo(id_rezervacije)
        flash("Rezervacija je bila izbrisana.", "success")
    except Exception:
        flash("Napaka pri brisanju rezervacije.", "error")
    return redirect('/rezervacije')