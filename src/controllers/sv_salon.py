from flask import render_template, request, redirect, abort, session, flash
from models import model_salon
from models import model_rezervacije


def pregled():
    return redirect('/saloni')


def seznam_stranke():
    stranke = model_salon.get_stranke()
    return render_template("seznam_stranke.html", stranke=stranke)


def salon_detail(salon_id):
    try:
        salon = model_salon.get_salon_by_id(salon_id)
    except Exception:
        salon = None

    if salon is None:
        abort(404)

    try:
        storitve = model_salon.get_storitve_za_salon(salon_id)
    except Exception:
        storitve = []

    return render_template("salon.html", salon=salon, storitve=storitve, ocene=[])


def saloni_view():
    return render_template("saloni_view.html", saloni=model_salon.get_salone())


def urnik():
    if request.method == 'POST':
        try:
            model_salon.dodaj_urnik(
                request.form.get('frizer_id'),
                request.form.get('dan'),
                request.form.get('ura')
            )
            flash("Urnik je bil uspešno dodan.", "success")
        except ValueError as e:
            flash(str(e), "error")
        except Exception:
            flash("Napaka pri dodajanju urnika. Poskusi znova.", "error")
        return redirect('/urnik')

    return render_template("urnik.html",
                           urnik=model_salon.get_urnik(),
                           frizerji=model_salon.get_frizerje())


def zgodovina():
    rezervacije = model_salon.get_rezervacije()
    return render_template("zgodovina.html", rezervacije=rezervacije)


def frizer():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("frizer", "admin"):
        return "Nimaš dostopa.", 403

    # show all reservations for now
    # in future: filter by this frizer's id
    rezervacije = model_rezervacije.get_vse_rezervacije()
    return render_template("frizer_panel.html", rezervacije=rezervacije)