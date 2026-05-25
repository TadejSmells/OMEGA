from flask import redirect, flash, session
from models import model_preklic_rezervacije as model
import db


def _get_frizer_id():
    """Pomožna: vrne id_frizer iz tabele frizer za prijavljenega userja."""
    user_id = session.get('user_id')
    db_session = db.get_session()
    try:
        from models.models import Frizer
        frizer = db_session.query(Frizer).filter(Frizer.user_id == user_id).first()
        return frizer.id_frizer if frizer else None
    finally:
        db_session.close()

def preklic_rezervacije(id_rezervacije):
    """Prekliče rezervacijo — samo če pripada prijavljenemu frizerju."""
    frizer_id = _get_frizer_id()
    if frizer_id is None:
        flash("Frizerjev račun ni najden.", "error")
        return redirect('/frizer')

    uspeh = model.preklic_rezervacije_frizerja(id_rezervacije, frizer_id)
    if uspeh:
        flash("Rezervacija je bila preklicana.", "success")
    else:
        flash("Rezervacija ni bila najdena ali nimate dovoljenja.", "error")
    return redirect('/frizer')
