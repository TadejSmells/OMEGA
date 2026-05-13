# Primer modela — predloga za nove model datoteke

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
# from models.models import TvojaTabela  ← importaj pravi model


def get_vse_podatke():
    """
    Primer: vrne vse vrstice iz tabele.
    Zamenjaj Tabela z dejanskim modelom iz models.py.
    """
    session = db.get_session()
    try:
        # rows = session.query(TvojaTabela).all()
        # return rows
        pass
    finally:
        session.close()


# Vzorec za insert:
def dodaj_zapis(podatek1, podatek2):
    session = db.get_session()
    try:
        # session.add(TvojaTabela(polje1=podatek1, polje2=podatek2))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
