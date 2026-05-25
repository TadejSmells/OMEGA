from flask import render_template, request, redirect, flash, session, abort
from models import model_uredi_salon


def uredi_salon(salon_id):
    """Admin only — uredi informacije obstoječega salona."""
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    salon = model_uredi_salon.get_salon(salon_id)
    if salon is None:
        abort(404)

    if request.method == "POST":
        ime     = request.form.get("ime", "").strip()
        naslov  = request.form.get("naslov", "").strip()
        mesto   = request.form.get("mesto", "").strip()
        telefon = request.form.get("telefon", "").strip()

        if not ime:
            flash("Ime salona je obvezno.", "error")
            return redirect(f"/saloni/uredi/{salon_id}")

        try:
            uspeh = model_uredi_salon.update_salon(salon_id, ime, naslov, mesto, telefon)
            if uspeh:
                flash(f"Salon '{ime}' je bil uspešno posodobljen.", "success")
                return redirect("/saloni")
            else:
                flash("Salon ni bil najden.", "error")
                return redirect("/saloni")
        except ValueError as e:
            flash(str(e), "error")
            return redirect(f"/saloni/uredi/{salon_id}")
        except Exception:
            flash("Napaka pri shranjevanju. Poskusi znova.", "error")
            return redirect(f"/saloni/uredi/{salon_id}")

    return render_template("uredi_salon.html", salon=salon)
