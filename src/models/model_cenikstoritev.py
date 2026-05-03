import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Storitev


def get_vse_storitve():
    session = db.get_session()
    try:
        rows = session.query(Storitev).order_by(Storitev.id_storitve).all()
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()


def dodaj_storitev(ime_storitve, cena, trajanje):
    """
    Doda novo storitev v bazo.
    Vrže ValueError če storitev s tem imenom že obstaja.
    """
    db_session = db.get_session()
    try:
        obstoječa = db_session.query(Storitev).filter(
            Storitev.ime_storitve == ime_storitve
        ).first()
        if obstoječa:
            raise ValueError(f"Storitev '{ime_storitve}' že obstaja.")

        db_session.add(Storitev(
            ime_storitve=ime_storitve,
            cena=cena,
            trajanje=trajanje
        ))
        db_session.commit()
    except ValueError:
        raise
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()