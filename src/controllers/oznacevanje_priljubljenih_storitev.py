from flask import session, redirect, request, flash
from models import model_oznacevanje_priljubljenih_storitev as model_priljubljene_storitve


def toggle_priljubljeno(id_storitve):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "stranka":
        flash("Samo prijavljene stranke lahko označijo storitev kot priljubljeno.", "error")
        return redirect("/storitve")

    try:
        je_sedaj = model_priljubljene_storitve.toggle_priljubljeno(
            session["user_id"], id_storitve
        )
        if je_sedaj:
            flash("Storitev je dodana med priljubljene. ❤", "success")
        else:
            flash("Storitev je odstranjena iz priljubljenih.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        flash("Napaka pri označevanju priljubljene storitve. Poskusi znova.", "error")

    # Vrni se nazaj, od koder si prišel (default /storitve)
    next_url = request.form.get("next") or request.referrer or "/storitve"
    return redirect(next_url)
