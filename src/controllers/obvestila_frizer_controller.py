from flask import session, redirect, flash
from models import model_obvestila_frizer
import db


def _get_frizer_id():
    user_id = session.get('user_id')
    if not user_id:
        return None
    s = db.get_session()
    try:
        from models.models import Frizer
        f = s.query(Frizer).filter(Frizer.user_id == user_id).first()
        return f.id_frizer if f else None
    finally:
        s.close()


def obvestila_za_frizerja():
    """Jinja global — kliče se direktno iz frizer.html."""
    frizer_id = _get_frizer_id()
    if frizer_id is None:
        return []
    try:
        return model_obvestila_frizer.sinhroniziraj_in_vrni(frizer_id)
    except Exception:
        return []


def opusti_obvestilo(id_sporocila):
    """POST handler za dismiss."""
    frizer_id = _get_frizer_id()
    if frizer_id is None:
        flash("Frizerjev račun ni najden.", "error")
        return redirect('/frizer')
    model_obvestila_frizer.oznaci_prebrano(id_sporocila, frizer_id)
    return redirect('/frizer')