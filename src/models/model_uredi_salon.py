import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Salon


def get_salon(salon_id):
    """Vrne podatke o enem salonu po ID-ju (kot dict)."""
    session = db.get_session()
    try:
        s = session.query(Salon).filter(Salon.id == salon_id).first()
        if s is None:
            return None
        return {
            "id": s.id,
            "ime": s.ime,
            "naslov": s.naslov,
            "mesto": s.mesto,
            "telefon": s.telefon,
        }
    finally:
        session.close()


def update_salon(salon_id, ime, naslov, mesto, telefon):
    """
    Posodobi podatke salona. Vrne True ob uspehu, False če salon ne obstaja.
    Vrže ValueError, če je ime prazno.
    """
    if not ime or not ime.strip():
        raise ValueError("Ime salona je obvezno.")

    session = db.get_session()
    try:
        s = session.query(Salon).filter(Salon.id == salon_id).first()
        if s is None:
            return False

        s.ime = ime.strip()
        s.naslov = (naslov or "").strip() or None
        s.mesto = (mesto or "").strip() or None
        s.telefon = (telefon or "").strip() or None

        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
