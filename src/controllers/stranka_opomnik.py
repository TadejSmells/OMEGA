from flask import session
from models import model_stranka_opomnik as model_opomnik


def get_danasnje_rezervacije(user_id):
    """Vrne seznam današnjih aktivnih rezervacij stranke."""
    return model_opomnik.get_danasnje_rezervacije_stranke(user_id)


def opomnik_po_prijavi():
    """Stara funkcija — ohranjena za združljivost."""
    user_id = session.get('user_id')
    vloga   = session.get('role')
    if vloga != 'stranka' or not user_id:
        return None
    return model_opomnik.get_danasnje_rezervacije_stranke(user_id)