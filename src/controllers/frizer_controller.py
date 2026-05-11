from flask import render_template, abort, request, redirect, flash, session
from models import model_frizer


def frizer_profil(frizer_id):
    """Prikaže osebno stran posameznega frizerja."""
    frizer = model_frizer.get_frizer(frizer_id)

    if frizer is None:
        abort(404)

    salon = model_frizer.get_salon_frizerja(frizer_id)
    storitve = model_frizer.get_storitve_frizerja(frizer_id)

    return render_template(
        "frizer_profil.html",
        frizer=frizer,
        salon=salon,
        storitve=storitve
    )


def seznam_frizerjev():
    """Prikaže seznam vseh frizerjev."""
    frizerji = model_frizer.get_vsi_frizerji()

    return render_template(
        "seznam_frizerjev.html",
        frizerji=frizerji
    )


def dodaj_frizer():
    """Admin only — doda novega frizerja."""
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    if request.method == "POST":
        ime     = request.form.get("ime", "").strip()
        kontakt = request.form.get("kontakt", "").strip()
        salon_id = request.form.get("salon_id") or None

        if not ime:
            flash("Ime frizerja je obvezno.", "error")
            return redirect("/frizerji/dodaj")

        try:
            model_frizer.dodaj_frizer(ime, kontakt, salon_id)
            flash(f"Frizer '{ime}' je bil uspešno dodan.", "success")
            return redirect("/frizerji")
        except ValueError as e:
            flash(str(e), "error")
            return redirect("/frizerji/dodaj")
        except Exception:
            flash("Napaka pri dodajanju frizerja. Poskusi znova.", "error")
            return redirect("/frizerji/dodaj")

    saloni = model_frizer.get_vsi_saloni()
    return render_template("dodaj_frizer.html", saloni=saloni)