"""
model_priljubljeni.py — Model za priljubljene salone.

Priljubljenost je vezana na id_stranke za navadne stranke.
Za frizerje in adminov (ki nimajo vrstice v tabeli stranka) pa
se uporabi negativni user_id kot nadomestni id_stranke,
da se izognemo spremembi sheme baze.
Vrednost: -user_id (vedno negativna, zato ne trči z obstoječimi id_stranke).
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import PriljubljeniSaloni, Stranka


def _get_fav_key(user_id):
    """
    Vrne ključ za priljubljeni_saloni tabelo za kateregakoli prijavljenega
    uporabnika — ne glede na vlogo.

    - Stranke:        vrne njihov pravi id_stranke (pozitivno število)
    - Frizerji/admini: nimajo vrstice v tabeli stranka, zato vrne -user_id
                       (negativno število, ki ne trči z obstoječimi id-ji)
    """
    if not user_id:
        return None
    db_session = db.get_session()
    try:
        stranka = db_session.query(Stranka).filter(
            Stranka.user_id == user_id
        ).first()
        return stranka.id_stranke if stranka else -user_id
    finally:
        db_session.close()


# Keep old name for backwards compatibility with any code that calls it directly
def get_id_stranke(user_id):
    return _get_fav_key(user_id)


def get_priljubljene_ids(user_id):
    """
    Vrne set id-jev salonov, ki jih je uporabnik označil kot priljubljene.
    Deluje za vse vloge (stranka, frizer, admin).
    """
    if not user_id:
        return set()

    fav_key = _get_fav_key(user_id)
    if fav_key is None:
        return set()

    db_session = db.get_session()
    try:
        rows = db_session.query(PriljubljeniSaloni).filter(
            PriljubljeniSaloni.id_stranke == fav_key
        ).all()
        return {r.id_salona for r in rows}
    finally:
        db_session.close()


def toggle_priljubljenega(fav_key, salon_id):
    """
    Preklopi priljubljenost salona.
    fav_key je vrednost iz _get_fav_key() — bodisi id_stranke bodisi -user_id.
    """
    db_session = db.get_session()
    try:
        obstoječ = db_session.query(PriljubljeniSaloni).filter(
            PriljubljeniSaloni.id_stranke == fav_key,
            PriljubljeniSaloni.id_salona == salon_id
        ).first()

        if obstoječ:
            db_session.delete(obstoječ)
        else:
            db_session.add(PriljubljeniSaloni(
                id_stranke=fav_key,
                id_salona=int(salon_id)
            ))

        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def get_priljubljene_salone(user_id):
    """
    Vrne seznam vseh priljubljenih salonov za prijavljenega uporabnika.
    Vsaka vrstica: (id, ime, naslov, mesto, telefon).
    Deluje za vse vloge.
    """
    if not user_id:
        return []

    fav_key = _get_fav_key(user_id)
    if fav_key is None:
        return []

    from models.models import Salon
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(Salon)
            .join(PriljubljeniSaloni, Salon.id == PriljubljeniSaloni.id_salona)
            .filter(PriljubljeniSaloni.id_stranke == fav_key)
            .order_by(Salon.ime)
            .all()
        )
        return [(s.id, s.ime, s.naslov, s.mesto, s.telefon) for s in rows]
    finally:
        db_session.close()