
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import KomentarSalona, Salon, Stranka


def get_stranka_id(user_id):
    session = db.get_session()
    try:
        row = session.query(Stranka.id_stranke).filter(Stranka.user_id == user_id).first()
        if row:
            return row[0]
        else:
            return None
    finally:
        session.close()
#ok zgornja koda pac gre in iz sessiona, 
#torej ko se je stranka PRIJAVLJENA returna ta id, 
#ker bo LE prijavljena stranka dodajala komentar

def dodaj_komentar(salon_id, id_stranke, ocena, komentar):
    try:
        ocena = int(ocena)
    except (TypeError, ValueError):
        raise ValueError("Ocena mora biti število med 1 in 5.")
    if ocena < 1 or ocena > 5:
        raise ValueError("Ocena mora biti med 1 in 5.")

    komentar = (komentar or "").strip() or None

    session = db.get_session()
    try:
        session.add(KomentarSalona(
            id_salona=salon_id,
            id_stranke=id_stranke,
            ocena=ocena,
            komentar=komentar,
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_komentarji_salona(salon_id):
    """Vrne seznam komentarjev za salon, z imenom stranke."""
    session = db.get_session()
    try:
        rows = (
            session.query(
                KomentarSalona.ocena,
                KomentarSalona.komentar,
                KomentarSalona.datum,
                Stranka.ime,
                Stranka.priimek,
            )
            .join(Stranka, KomentarSalona.id_stranke == Stranka.id_stranke)
            .filter(KomentarSalona.id_salona == salon_id)
            .order_by(KomentarSalona.datum.desc())
            .all()
        )
        return rows
    finally:
        session.close()