from flask import session
from models import model_frizer_opomnik as model_opomnik


def get_danasnje_rezervacije(user_id):
    """Vrne seznam današnjih aktivnih rezervacij frizerja."""
    return model_opomnik.get_danasnje_rezervacije_frizerja(user_id)


def opomnik_po_prijavi():
    """Vrne rezervacije če je prijavljen frizer."""
    user_id = session.get('user_id')
    vloga   = session.get('role')
    if vloga not in ('frizer', 'admin') or not user_id:
        return None
    return model_opomnik.get_danasnje_rezervacije_frizerja(user_id)