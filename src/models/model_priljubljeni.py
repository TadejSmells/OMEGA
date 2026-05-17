"""
model_priljubljeni.py — Model za priljubljene salone, frizerje in storitve.

Zakaj obstaja ta datoteka:
    Uporabniki (stranke) lahko označijo salone kot priljubljene.
    Ta model skrbi za shranjevanje, brisanje in pridobivanje teh podatkov
    iz baze. Vse operacije so vezane na id_stranke, ki se pridobi
    iz prijavljenega user_id prek tabele stranka.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import PriljubljeniSaloni, Stranka


def get_id_stranke(user_id):
    """
    Pretvori user_id (iz Flask session) v id_stranke (iz tabele stranka).
    Vrne None če stranka ne obstaja za tega uporabnika.

    Zakaj:
        Session hrani user_id iz tabele users, toda priljubljeni_saloni
        se veže na id_stranke iz tabele stranka. Ta funkcija naredi most
        med obema tabelama.
    """
    db_session = db.get_session()
    try:
        stranka = db_session.query(Stranka).filter(
            Stranka.user_id == user_id
        ).first()
        return stranka.id_stranke if stranka else None
    finally:
        db_session.close()


def get_priljubljene_ids(user_id):
    """
    Vrne set id-jev salonov, ki jih je uporabnik označil kot priljubljene.
    Vrne prazen set če uporabnik ni prijavljen ali nima nobenih priljubljenih.

    Zakaj:
        Template potrebuje to informacijo da obarva zvezdo na vsaki salon
        kartici — aktivna (črna) če je priljubljen, neaktivna (siva) če ni.
        Set omogoča O(1) preverjanje: `if salon_id in priljubljeni_ids`.
    """
    if not user_id:
        return set()

    id_stranke = get_id_stranke(user_id)
    if not id_stranke:
        return set()

    db_session = db.get_session()
    try:
        rows = db_session.query(PriljubljeniSaloni).filter(
            PriljubljeniSaloni.id_stranke == id_stranke
        ).all()
        return {r.id_salona for r in rows}
    finally:
        db_session.close()


def toggle_priljubljenega(id_stranke, salon_id):
    """
    Preklopi priljubljenost salona za stranko.
    Če salon še ni priljubljen — ga doda.
    Če salon že je priljubljen — ga odstrani.

    Zakaj:
        En endpoint za obe operaciji je čistejši kot ločena add/remove.
        Klient ne rabi vedeti ali je salon že priljubljen — samo pošlje
        POST in backend sam ugotovi kaj narediti.
    """
    db_session = db.get_session()
    try:
        obstoječ = db_session.query(PriljubljeniSaloni).filter(
            PriljubljeniSaloni.id_stranke == id_stranke,
            PriljubljeniSaloni.id_salona == salon_id
        ).first()

        if obstoječ:
            db_session.delete(obstoječ)
        else:
            db_session.add(PriljubljeniSaloni(
                id_stranke=id_stranke,
                id_salona=int(salon_id)
            ))

        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def get_priljubljene_salone(user_id):
    """
    Vrne seznam vseh priljubljenih salonov za prijavljenega uporabnika.
    Vsaka vrstica: (id, ime, naslov, mesto, telefon).

    Zakaj:
        Stran /priljubljeni_saloni potrebuje polne podatke o salonih,
        ne samo njihove ID-je. Ta funkcija naredi JOIN med
        priljubljeni_saloni in salon tabelama v eni poizvedbi.
    """
    if not user_id:
        return []

    id_stranke = get_id_stranke(user_id)
    if not id_stranke:
        return []

    from models.models import Salon
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(Salon)
            .join(PriljubljeniSaloni, Salon.id == PriljubljeniSaloni.id_salona)
            .filter(PriljubljeniSaloni.id_stranke == id_stranke)
            .order_by(Salon.ime)
            .all()
        )
        return [(s.id, s.ime, s.naslov, s.mesto, s.telefon) for s in rows]
    finally:
        db_session.close()
