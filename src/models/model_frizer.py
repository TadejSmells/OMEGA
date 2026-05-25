import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Frizer, Salon, Storitev, Stranka, SaloniInStoritve, KomentarFrizerja

def get_frizer(frizer_id):
    session = db.get_session()
    try:
        frizer = session.query(Frizer).filter(Frizer.id_frizer == frizer_id).first()
        if frizer is None:
            return None
        return {
            "id": frizer.id_frizer,
            "ime": frizer.ime,
            "kontakt": frizer.kontakt,
            "salon_id": frizer.salon_id
        }
    finally:
        session.close()


def get_salon_frizerja(frizer_id):
    session = db.get_session()
    try:
        rezultat = (
            session.query(Salon)
            .join(Frizer, Frizer.salon_id == Salon.id)
            .filter(Frizer.id_frizer == frizer_id)
            .first()
        )
        if rezultat is None:
            return None
        return {
            "id": rezultat.id,
            "ime": rezultat.ime,
            "naslov": rezultat.naslov,
            "mesto": rezultat.mesto,
            "telefon": rezultat.telefon
        }
    finally:
        session.close()


def get_storitve_frizerja(frizer_id):
    session = db.get_session()
    try:
        frizer = session.query(Frizer).filter(Frizer.id_frizer == frizer_id).first()
        if frizer is None or frizer.salon_id is None:
            return []
        rows = (
            session.query(Storitev)
            .join(SaloniInStoritve, Storitev.id_storitve == SaloniInStoritve.storitev_id)
            .filter(SaloniInStoritve.salon_id == frizer.salon_id)
            .order_by(Storitev.ime_storitve)
            .all()
        )
        return [
            {
                "id": r.id_storitve,
                "ime": r.ime_storitve,
                "cena": float(r.cena) if r.cena else None,
                "trajanje": str(r.trajanje) if r.trajanje else None
            }
            for r in rows
        ]
    finally:
        session.close()


def get_vsi_frizerji():
    session = db.get_session()
    try:
        rows = (
            session.query(Frizer, Salon)
            .outerjoin(Salon, Frizer.salon_id == Salon.id)
            .order_by(Frizer.id_frizer)
            .all()
        )
        return [
            {
                "id": f.id_frizer,
                "ime": f.ime,
                "kontakt": f.kontakt,
                "salon": s.ime if s else "—",
                "salon_id": s.id if s else None
            }
            for f, s in rows
        ]
    finally:
        session.close()


def get_vsi_saloni():
    session = db.get_session()
    try:
        rows = session.query(Salon).order_by(Salon.ime).all()
        return [{"id": s.id, "ime": s.ime} for s in rows]
    finally:
        session.close()


def dodaj_frizer(ime, kontakt, salon_id):
    db_session = db.get_session()
    try:
        obstoječ = db_session.query(Frizer).filter(Frizer.ime == ime).first()
        if obstoječ:
            raise ValueError(f"Frizer z imenom '{ime}' že obstaja.")
        db_session.add(Frizer(
            ime=ime,
            kontakt=kontakt or None,
            salon_id=salon_id or None
        ))
        db_session.commit()
    except ValueError:
        raise
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def get_komentarji_frizerja(frizer_id):
    """Vrne vse komentarje za frizerja, najnovejši prvi."""
    session = db.get_session()
    try:
        rows = (
            session.query(KomentarFrizerja, Stranka)
            .outerjoin(Stranka, KomentarFrizerja.id_stranke == Stranka.id_stranke)
            .filter(KomentarFrizerja.id_frizerja == frizer_id)
            .order_by(KomentarFrizerja.datum.desc())
            .all()
        )
        return [
            {
                "id": k.id_komentar,
                "ocena": k.ocena,
                "komentar": k.komentar,
                "datum": k.datum.strftime("%d. %m. %Y") if k.datum else "—",
                "avtor": f"{s.ime} {s.priimek}" if s and s.ime else (s.priimek if s else "Anonimno")
            }
            for k, s in rows
        ]
    finally:
        session.close()


def dodaj_komentar_frizerja(frizer_id, stranka_id, ocena, komentar):
    """
    Doda komentar frizerju.
    Vrže ValueError če ocena ni med 1 in 5.
    """
    try:
        ocena = int(ocena)
    except (TypeError, ValueError):
        raise ValueError("Ocena mora biti celo število med 1 in 5.")

    if not (1 <= ocena <= 5):
        raise ValueError("Ocena mora biti med 1 in 5.")

    if not komentar or not komentar.strip():
        raise ValueError("Komentar ne sme biti prazen.")

    db_session = db.get_session()
    try:
        db_session.add(KomentarFrizerja(
            id_frizerja=frizer_id,
            id_stranke=stranka_id,
            ocena=ocena,
            komentar=komentar.strip()
        ))
        db_session.commit()
    except ValueError:
        raise
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()
