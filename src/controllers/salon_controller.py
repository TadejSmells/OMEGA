from flask import render_template, request, redirect, flash, session
from models import model_salon


def dodaj_salon():
    """Admin only — doda nov salon."""
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    if request.method == "POST":
        ime     = request.form.get("ime", "").strip()
        naslov  = request.form.get("naslov", "").strip()
        mesto   = request.form.get("mesto", "").strip()
        telefon = request.form.get("telefon", "").strip()

        if not ime:
            flash("Ime salona je obvezno.", "error")
            return redirect("/saloni/dodaj")

        try:
            model_salon.dodaj_salon(ime, naslov, mesto, telefon)
            flash(f"Salon '{ime}' je bil uspešno dodan.", "success")
            return redirect("/saloni")
        except ValueError as e:
            flash(str(e), "error")
            return redirect("/saloni/dodaj")
        except Exception:
            flash("Napaka pri dodajanju salona. Poskusi znova.", "error")
            return redirect("/saloni/dodaj")

    return render_template("dodaj_salon.html")
