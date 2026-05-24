import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import KomentarStoritve, Storitev, Stranka


def get_stranka_id(user_id):
    """Vrne id_stranke za prijavljenega uporabnika, ali None."""
    session = db.get_session()
    try:
        row = session.query(Stranka.id_stranke).filter(Stranka.user_id == user_id).first()
        return row[0] if row else None
    finally:
        session.close()


def get_storitev(storitev_id):
    """Vrne osnovne podatke o storitvi (id, ime, cena, trajanje, opis)."""
    session = db.get_session()
    try:
        return (
            session.query(
                Storitev.id_storitve,
                Storitev.ime_storitve,
                Storitev.cena,
                Storitev.trajanje,
                Storitev.opis,
            )
            .filter(Storitev.id_storitve == storitev_id)
            .first()
        )
    finally:
        session.close()


def dodaj_komentar(storitev_id, id_stranke, ocena, komentar):
    """Doda komentar storitvi. Vrže ValueError pri neveljavni oceni/komentarju."""
    try:
        ocena = int(ocena)
    except (TypeError, ValueError):
        raise ValueError("Ocena mora biti število med 1 in 5.")
    if ocena < 1 or ocena > 5:
        raise ValueError("Ocena mora biti med 1 in 5.")

    komentar = (komentar or "").strip() or None

    session = db.get_session()
    try:
        session.add(KomentarStoritve(
            id_storitve=storitev_id,
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


def get_komentarji_storitve(storitev_id):
    """Vrne komentarje za storitev (ocena, komentar, datum, ime, priimek), najnovejši prvi."""
    session = db.get_session()
    try:
        rows = (
            session.query(
                KomentarStoritve.ocena,
                KomentarStoritve.komentar,
                KomentarStoritve.datum,
                Stranka.ime,
                Stranka.priimek,
            )
            .outerjoin(Stranka, KomentarStoritve.id_stranke == Stranka.id_stranke)
            .filter(KomentarStoritve.id_storitve == storitev_id)
            .order_by(KomentarStoritve.datum.desc())
            .all()
        )
        return rows
    finally:
        session.close()
