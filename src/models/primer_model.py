# PRIMER MODELA — kako mora izgledati model datoteka
# Kopiraj ta vzorec ko delaš svojo model datoteko

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
# from models.models import TvojModel  ← importaj svojo tabelo iz models.py


def get_vse_podatke():
    """
    Primer funkcije ki dobi vse podatke iz tabele.
    Zamenjaj 'TvojModel' z dejanskim imenom razreda iz models.py
    """
    session = db.get_session()
    try:
        # rows = session.query(TvojModel).all()
        # return [(r.id, r.ime) for r in rows]
        return []  # zamenjaj z zgornjo kodo
    finally:
        session.close()