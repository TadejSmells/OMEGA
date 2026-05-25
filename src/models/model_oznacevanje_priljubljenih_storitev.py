import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import PriljubljeneStoritve, Stranka, Storitev


def _stranka_id_iz_user_id(session, user_id):
    if not user_id:
        return None
    stranka = session.query(Stranka).filter(Stranka.user_id == user_id).first()
    return stranka.id_stranke if stranka else None


def get_priljubljene_ids(user_id):
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            return set()
        rows = (
            session.query(PriljubljeneStoritve.id_storitve)
            .filter(PriljubljeneStoritve.id_stranke == id_stranke)
            .all()
        )
        return {r[0] for r in rows}
    finally:
        session.close()


def je_priljubljena(user_id, id_storitve):
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            return False
        return session.query(PriljubljeneStoritve).filter(
            PriljubljeneStoritve.id_stranke == id_stranke,
            PriljubljeneStoritve.id_storitve == id_storitve
        ).first() is not None
    finally:
        session.close()


def toggle_priljubljeno(user_id, id_storitve):
    
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            raise ValueError("Uporabnik nima povezane stranke.")

        # Preveri, da storitev obstaja (preprečimo dangling FK)
        obstaja = session.query(Storitev).filter(
            Storitev.id_storitve == id_storitve
        ).first()
        if not obstaja:
            raise ValueError("Storitev ne obstaja.")

        obstoječa = session.query(PriljubljeneStoritve).filter(
            PriljubljeneStoritve.id_stranke == id_stranke,
            PriljubljeneStoritve.id_storitve == id_storitve
        ).first()

        if obstoječa:
            session.delete(obstoječa)
            session.commit()
            return False
        else:
            session.add(PriljubljeneStoritve(
                id_stranke=id_stranke,
                id_storitve=id_storitve
            ))
            session.commit()
            return True
    except ValueError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def dodaj_priljubljeno(user_id, id_storitve):
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            raise ValueError("Uporabnik nima povezane stranke.")

        obstoječa = session.query(PriljubljeneStoritve).filter(
            PriljubljeneStoritve.id_stranke == id_stranke,
            PriljubljeneStoritve.id_storitve == id_storitve
        ).first()
        if obstoječa:
            return  # že obstaja, nič za narediti

        session.add(PriljubljeneStoritve(
            id_stranke=id_stranke,
            id_storitve=id_storitve
        ))
        session.commit()
    except ValueError:
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def odstrani_priljubljeno(user_id, id_storitve):
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            return

        session.query(PriljubljeneStoritve).filter(
            PriljubljeneStoritve.id_stranke == id_stranke,
            PriljubljeneStoritve.id_storitve == id_storitve
        ).delete()
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_priljubljene_storitve(user_id):
    session = db.get_session()
    try:
        id_stranke = _stranka_id_iz_user_id(session, user_id)
        if id_stranke is None:
            return []
        rows = (
            session.query(Storitev)
            .join(
                PriljubljeneStoritve,
                PriljubljeneStoritve.id_storitve == Storitev.id_storitve,
            )
            .filter(PriljubljeneStoritve.id_stranke == id_stranke)
            .order_by(Storitev.ime_storitve)
            .all()
        )
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()