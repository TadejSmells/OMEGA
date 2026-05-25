from flask import request, redirect, session, flash
from models import model_frizer
from models import komentar_salona  # reuse get_stranka_id(user_id) -> id_stranke


def dodaj(frizer_id):
    """POST handler za dodajanje komentarja frizerju — samo prijavljene stranke."""
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "stranka":
        flash("Komentarje lahko dodajajo samo stranke.", "error")
        return redirect(f"/frizer/{frizer_id}")

    # user_id (users.id) != id_stranke (stranka.id_stranke) — poišči pravi id_stranke
    id_stranke = komentar_salona.get_stranka_id(session["user_id"])
    if id_stranke is None:
        flash("Vašega profila stranke ni mogoče najti.", "error")
        return redirect(f"/frizer/{frizer_id}")

    try:
        model_frizer.dodaj_komentar_frizerja(
            frizer_id,
            id_stranke,
            request.form.get("ocena"),
            request.form.get("komentar", ""),
        )
        flash("Komentar je bil uspešno dodan.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        flash("Napaka pri dodajanju komentarja. Poskusi znova.", "error")

    return redirect(f"/frizer/{frizer_id}")
