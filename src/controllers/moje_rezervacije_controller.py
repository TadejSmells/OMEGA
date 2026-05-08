from flask import render_template, request, redirect, flash, session
from models import model_moje_rezervacije


def _get_stranka_id():
    """Pomožna: iz seje pridobi id_stranke, ali None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return model_moje_rezervacije.get_stranka_id_za_user(user_id)


def moje_rezervacije():
    """Prikaže seznam vseh strankinih rezervacij."""
    id_stranke = _get_stranka_id()
    if not id_stranke:
        flash("Dostop samo za stranke.", "error")
        return redirect('/login')

    rezervacije = model_moje_rezervacije.get_moje_rezervacije(id_stranke)
    return render_template(
        "moje_rezervacije.html",
        rezervacije=rezervacije,
    )


def uredi_mojo_rezervacijo(id_rezervacije):
    """GET: prikaže formo za urejanje. POST: shrani spremembe."""
    id_stranke = _get_stranka_id()
    if not id_stranke:
        flash("Dostop samo za stranke.", "error")
        return redirect('/login')

    rezervacija = model_moje_rezervacije.get_mojo_rezervacijo(id_rezervacije, id_stranke)
    if rezervacija is None:
        flash("Rezervacija ne obstaja ali nimate dostopa.", "error")
        return redirect('/moje_rezervacije')

    if rezervacija[7] == 'cancelled':
        flash("Preklicane rezervacije ni mogoče urejati.", "error")
        return redirect('/moje_rezervacije')

    if request.method == 'POST':
        frizer_id   = request.form.get('frizer_id')   or None
        salon_id    = request.form.get('salon_id')    or None
        storitev_id = request.form.get('storitev_id') or None
        datum       = request.form.get('datum')       or None
        ura         = request.form.get('ura')         or None

        ok = model_moje_rezervacije.uredi_mojo_rezervacijo(
            id_rezervacije, id_stranke,
            frizer_id, salon_id, storitev_id, datum, ura
        )
        if ok:
            flash("Rezervacija uspešno posodobljena.", "success")
        else:
            flash("Urejanje ni uspelo (rezervacija je morda že preklicana).", "error")
        return redirect('/moje_rezervacije')

    return render_template(
        "moje_rezervacije_uredi.html",
        rezervacija=rezervacija,
        frizerji=model_moje_rezervacije.get_frizerje(),
        saloni=model_moje_rezervacije.get_salone(),
        storitve=model_moje_rezervacije.get_storitve(),
    )


def preklic_moje_rezervacije(id_rezervacije):
    """POST: nastavi status na cancelled."""
    id_stranke = _get_stranka_id()
    if not id_stranke:
        flash("Dostop samo za stranke.", "error")
        return redirect('/login')

    ok = model_moje_rezervacije.preklic_moje_rezervacije(id_rezervacije, id_stranke)
    if ok:
        flash("Rezervacija je bila preklicana.", "success")
    else:
        flash("Preklic ni uspel (rezervacija ni vaša ali je že preklicana).", "error")
    return redirect('/moje_rezervacije')
