from flask import render_template, request, redirect, abort, session, flash
from models import komentar_storitve as model


def storitev_detail(storitev_id):
    """Prikaže podrobnosti storitve s komentarji."""
    storitev = model.get_storitev(storitev_id)
    if storitev is None:
        abort(404)

    try:
        komentarji = model.get_komentarji_storitve(storitev_id)
    except Exception:
        komentarji = []

    povprecje = (
        round(sum(k.ocena for k in komentarji) / len(komentarji), 1)
        if komentarji else None
    )

    return render_template(
        "storitev_detail.html",
        storitev=storitev,
        komentarji=komentarji,
        povprecje=povprecje,
    )


def dodaj_komentar_storitvi(storitev_id):
    """POST handler — samo prijavljene stranke lahko dodajo komentar storitvi."""
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "stranka":
        flash("Komentarje lahko dodajajo samo stranke.", "error")
        return redirect(f"/storitev/{storitev_id}")

    id_stranke = model.get_stranka_id(session["user_id"])
    if id_stranke is None:
        flash("Vašega profila stranke ni mogoče najti.", "error")
        return redirect(f"/storitev/{storitev_id}")

    try:
        model.dodaj_komentar(
            storitev_id=storitev_id,
            id_stranke=id_stranke,
            ocena=request.form.get("ocena"),
            komentar=request.form.get("komentar"),
        )
        flash("Komentar je bil shranjen. Hvala!", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        flash("Napaka pri shranjevanju komentarja. Poskusi znova.", "error")

    return redirect(f"/storitev/{storitev_id}")
