import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from datetime import datetime
from sqlalchemy import text
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_vse_rezervacije():
    session = db.get_session()
    try:
        rows = (
            session.query(
                Rezervacija.id_rezervacije,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Rezervacija.datum,
                Rezervacija.ura,
                Storitev.cena.label('cena'),
                Rezervacija.status,
            )
            .outerjoin(Stranka,  Rezervacija.id_stranke  == Stranka.id_stranke)
            .outerjoin(Frizer,   Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon,    Rezervacija.id_salona   == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
        return rows
    finally:
        session.close()


def get_stranka_za_user(user_id):
    """Vrne (id_stranke, ime, priimek) za prijavljenega userja, ali None."""
    session = db.get_session()
    try:
        row = (
            session.query(Stranka.id_stranke, Stranka.ime, Stranka.priimek)
            .filter(Stranka.user_id == user_id)
            .first()
        )
        return row  # (id_stranke, ime, priimek) ali None
    finally:
        session.close()


def get_storitve_za_salon(salon_id):
    """
    Storitve, ki jih ponuja izbrani salon (prek povezovalne tabele
    saloni_in_storitve). Vrne SAMO storitve, ki so dejansko vezane na ta salon
    — ne vec vseh storitev iz baze.
    """
    session = db.get_session()
    try:
        rows = session.execute(
            text("""
                SELECT s.id_storitve, s.ime_storitve, s.cena, s.trajanje, s.opis
                FROM storitev s
                JOIN saloni_in_storitve ss ON ss.storitev_id = s.id_storitve
                WHERE ss.salon_id = :salon_id
                ORDER BY s.ime_storitve
            """),
            {'salon_id': salon_id}
        ).fetchall()
        return rows
    finally:
        session.close()


def get_frizerje_za_salon(salon_id):
    """Vrne frizerje danega salona."""
    session = db.get_session()
    try:
        rows = (
            session.query(Frizer.id_frizer, Frizer.salon_id, Frizer.ime, Frizer.kontakt)
            .filter(Frizer.salon_id == salon_id)
            .order_by(Frizer.ime)
            .all()
        )
        return rows
    finally:
        session.close()


def je_termin_zaseden(frizer_id, datum, ura):
    """
    True, ce za danega frizerja na ta datum in uro ze obstaja AKTIVNA rezervacija.
    Ura se primerja na natancnost HH:MM (obrazec poslje npr. '14:00',
    v bazi pa je shranjena kot '14:00:00').
    """
    if not frizer_id or not datum or not ura:
        return False

    session = db.get_session()
    try:
        # datum normaliziraj v date objekt (obrazec poslje 'YYYY-MM-DD')
        try:
            d = datetime.strptime(str(datum)[:10], '%Y-%m-%d').date()
        except ValueError:
            d = datum  # pusti, naj pretvorbo opravi baza

        ura_hhmm = str(ura)[:5]

        ure = (
            session.query(Rezervacija.ura)
            .filter(Rezervacija.id_frizerja == frizer_id)
            .filter(Rezervacija.datum == d)
            .filter(Rezervacija.status == 'active')
            .all()
        )
        return any(str(u)[:5] == ura_hhmm for (u,) in ure)
    finally:
        session.close()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id, datum, ura):
    session = db.get_session()
    try:
        session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None,
            datum=datum,
            ura=ura,
            status='active',
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def izbrisi_rezervacijo(id_rezervacije):
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            session.delete(r)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def preklic_rezervacije(id_rezervacije):
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            r.status = 'cancelled'
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()