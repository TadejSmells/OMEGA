from models import model_stranka_opomnik as model_opomnik


def get_danasnje_rezervacije(user_id):
    """Vrne seznam današnjih aktivnih rezervacij stranke."""
    return model_opomnik.get_danasnje_rezervacije_stranke(user_id)