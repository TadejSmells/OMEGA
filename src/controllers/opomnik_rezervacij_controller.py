from models import model_opomnik_rezervacij as model_opomnik


def get_danasnje_rezervacije(user_id):
    """Vrne seznam današnjih aktivnih rezervacij frizerja."""
    return model_opomnik.get_danasnje_rezervacije_frizerja(user_id)