from flask import render_template, request, redirect, abort, session, flash
from models import komentar_salona
from models import komentar_salona as ks_model

def dodaj_komentar_salonu(salon_id):
    """POST handler — samo prijavljene stranke."""
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "stranka":
        flash("Komentarje lahko dodajajo samo stranke.", "error")
        return redirect(f"/salon/{salon_id}")

    id_stranke = komentar_salona.get_stranka_id(session["user_id"])
    if id_stranke is None:
        flash("Vašega profila stranke ni mogoče najti.", "error")
        return redirect(f"/salon/{salon_id}")

    try:
        komentar_salona.dodaj_komentar(
            salon_id=salon_id,
            id_stranke=id_stranke,
            ocena=request.form.get("ocena"),
            komentar=request.form.get("komentar"),
        )
        flash("Komentar je bil shranjen. Hvala!", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        flash("Napaka pri shranjevanju komentarja. Poskusi znova.", "error")

    return redirect(f"/salon/{salon_id}")