# ── PRIMER MODELA ─────────────────────────────────────────────────────────────
# Ta datoteka je VZOREC — pokaže kako mora izgledati model datoteka.
# Kopiraj ta vzorec ko delaš svojo model datoteko.
#
# PRAVILA:
# - Vedno importaj db na vrhu (sys.path.append + import db)
# - Vedno importaj svojo tabelo iz models.models
# - Vedno zapri db_session v finally bloku
# - Nikoli ne piši raw SQL — uporabi session.query()

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
# from models.models import TvojModel  # ← zamenjaj z dejanskim razredom


def get_vse_podatke():
    """
    Primer funkcije ki dobi vse podatke iz tabele.
    Zamenjaj komentar z dejansko kodo.
    """
    db_session = db.get_session()
    try:
        # rows = db_session.query(TvojModel).all()
        # return [(r.id, r.ime) for r in rows]
        return []  # ← zamenjaj z zgornjo kodo
    finally:
        db_session.close()


def dodaj_podatek(vrednost):
    """
    Primer funkcije ki doda nov zapis v bazo.
    """
    db_session = db.get_session()
    try:
        # db_session.add(TvojModel(polje=vrednost))
        # db_session.commit()
        pass  # ← zamenjaj z zgornjo kodo
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()