from db import get_session, engine
from models import Base, Frizer, Stranka, Rezervacija, Salon, Storitev, Urnik

def setup_db():
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
            return [(r.id_frizer, r.salon_id, r.ime, r.kontakt) for r in rows]
        elif tip == 'stranka':
            rows = session.query(Stranka).order_by(Stranka.id_stranke).all()
            return [(r.id_stranke, r.ime, r.priimek, r.mail, r.telefon) for r in rows]
        elif tip == 'rezervacija':
            rows = session.query(Rezervacija).order_by(Rezervacija.id_rezervacije).all()
            return [(r.id_rezervacije, r.id_stranke, r.id_frizerja, r.salon_id, r.storitev_id) for r in rows]
        elif tip == 'salon':
            rows = session.query(Salon).order_by(Salon.id_salona).all()
            return [(r.id_salona, r.ime, r.naslov, r.mesto, r.telefon) for r in rows]
        elif tip == 'storitev':
            rows = session.query(Storitev).order_by(Storitev.id_storitve).all()
            return [(r.id_storitve, r.ime, r.cena, r.trajanje) for r in rows]
        elif tip == 'urnik':
            rows = session.query(Urnik).order_by(Urnik.id_urnik).all()
            return [(r.id_urnik, r.id_frizerja, r.dan, r.ura) for r in rows]
        return []
    finally:
        session.close()


def dodaj_frizerja(ime, kontakt, salon_id=None):
    session = get_session()
    try:
        session.add(Frizer(ime=ime, kontakt=kontakt, salon_id=salon_id or None))
        session.commit()
    finally:
        session.close()


def dodaj_stranko(ime, priimek, mail, telefon, id_naj_frizer=None):
    session = get_session()
    try:
        session.add(Stranka(ime=ime, priimek=priimek or '',
                            mail=mail, telefon=telefon,
                            id_naj_frizer=id_naj_frizer or None))
        session.commit()
    finally:
        session.close()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id=None, storitev_id=None):
    session = get_session()
    try:
        session.add(Rezervacija(id_stranke=stranka_id, id_frizerja=frizer_id,
                                salon_id=salon_id or None,
                                storitev_id=storitev_id or None))
        session.commit()
    finally:
        session.close()


def dodaj_salon(ime, naslov, mesto, telefon):
    session = get_session()
    try:
        session.add(Salon(ime=ime, naslov=naslov, mesto=mesto, telefon=telefon))
        session.commit()
    finally:
        session.close()


def dodaj_storitev(ime, cena, trajanje):
    session = get_session()
    try:
        session.add(Storitev(ime=ime, cena=cena, trajanje=trajanje))
        session.commit()
    finally:
        session.close()


def dodaj_urnik(frizer_id, dan, ura):
    session = get_session()
    try:
        session.add(Urnik(id_frizerja=frizer_id, dan=dan, ura=ura))
        session.commit()
    finally:
        session.close()