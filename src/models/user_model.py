# TA DATOTEKA NI VEČ V UPORABI — IZBRIŠI JO
#
# Uporabnik je definiran v models/models.py kot razred Uporabnik.
# Tabela v bazi se imenuje 'users'.
#
# Za delo z uporabniki importaj:
#   from models.models import Uporabnik
#
# Primer:
#   session = db.get_session()
#   user = session.query(Uporabnik).filter(Uporabnik.username == 'test').first()