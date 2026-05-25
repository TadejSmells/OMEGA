from flask import render_template, request, redirect, flash, session, abort
from models import urejanje_storitev


def uredi_storitev(storitev_id):
    """Admin only — urejanje storitve."""

    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    storitev = urejanje_storitev.get_storitev(storitev_id)

    if storitev is None:
        abort(404)

    if request.method == "POST":

        naziv = request.form.get("naziv", "").strip()
        cena = request.form.get("cena", "").strip()
        trajanje = request.form.get("trajanje", "").strip()
        opis = request.form.get("opis", "").strip()

        if not naziv:
            flash("Naziv storitve je obvezen.", "error")
            return redirect(f"/storitve/uredi/{storitev_id}")

        try:

            uspeh = urejanje_storitev.update_storitev(
                storitev_id,
                naziv,
                cena,
                trajanje,
                opis
            )

            if uspeh:
                flash("Storitev je bila uspešno posodobljena.", "success")
                return redirect("/storitve")

            else:
                flash("Storitev ni bila najdena.", "error")
                return redirect("/storitve")

        except ValueError as e:
            flash(str(e), "error")
            return redirect(f"/storitve/uredi/{storitev_id}")

        except Exception:
            flash("Napaka pri shranjevanju.", "error")
            return redirect(f"/storitve/uredi/{storitev_id}")

    return render_template(
        "uredi_storitev.html",
        storitev=storitev
    )