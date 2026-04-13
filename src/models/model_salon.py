from db import get_session, engine
from models import Base, Frizer, Stranka, Rezervacija
import sqlalchemy as sa

def setup_db():
    # DDL: create tables if they don't exist (replaces creation.sql for new setups)
    Base.metadata.create_all(engine)

    session = get_session()
    try:
        if session.query(Frizer).count() == 0:
            session.add_all([
                Frizer(salon_id=None, ime='Marko Matos',  kontakt='041-111-222'),
                Frizer(salon_id=None, ime='Špela Škarje', kontakt='040-333-444'),
            ])

        if session.query(Stranka).count() == 0:
            session.add(Stranka(ime='Luka', priimek='Novak',
                                mail='luka@test.si', telefon='031-999-888'))
        session.commit()
    finally:
        session.close()
    return True


def get_vse(tip):
    session = get_session()
    try:
        if tip == 'frizer':
            rows = session.query(Frizer).order_by(Frizer.id_frizer).all()
            # Return same tuple shape as before: (id, salon_id, ime, kontakt)
            return [(r.id_frizer, r.salon_id, r.ime, r.kontakt) for r in rows]
        elif tip == 'stranka':
            rows = session.query(Stranka).order_by(Stranka.id_stranke).all()
            return [(r.id_stranke, r.ime, r.priimek, r.mail, r.telefon) for r in rows]
        elif tip == 'rezervacija':
            rows = session.query(Rezervacija).order_by(Rezervacija.id_rezervacije).all()
            return [(r.id_rezervacije, r.id_stranke, r.id_frizerja) for r in rows]
        return []
    finally:
        session.close()


def dodaj_frizerja(ime, kontakt):
    session = get_session()
    try:
        session.add(Frizer(ime=ime, kontakt=kontakt))
        session.commit()
    finally:
        session.close()


def dodaj_stranko(ime, priimek, mail, telefon):
    session = get_session()
    try:
        session.add(Stranka(ime=ime, priimek=priimek or '', mail=mail, telefon=telefon))
        session.commit()
    finally:
        session.close()


def dodaj_rezervacijo(stranka_id, frizer_id):
    session = get_session()
    try:
        session.add(Rezervacija(id_stranke=stranka_id, id_frizerja=frizer_id))
        session.commit()
    finally:
        session.close()