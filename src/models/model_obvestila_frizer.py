import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Sporocilo, Rezervacija, Stranka, Storitev


def _naslov(id_rezervacije):
    return f"Preklic rezervacije #{id_rezervacije}"


def sinhroniziraj_in_vrni(frizer_id):
    """
    1) Najde vse cancelled rezervacije tega frizerja brez Sporocila.
    2) Za vsako ustvari Sporocilo (prebrano=False).
    3) Vrne neprebrana obvestila o preklicih.
    """
    s = db.get_session()
    try:
        cancelled = (
            s.query(Rezervacija)
             .filter(
                 Rezervacija.id_frizerja == frizer_id,
                 Rezervacija.status == 'cancelled',
             )
             .all()
        )

        for r in cancelled:
            naslov = _naslov(r.id_rezervacije)
            obstaja = (
                s.query(Sporocilo)
                 .filter(
                     Sporocilo.id_frizerja == frizer_id,
                     Sporocilo.naslov == naslov,
                 )
                 .first()
            )
            if obstaja:
                continue

            stranka = s.query(Stranka).filter(
                Stranka.id_stranke == r.id_stranke
            ).first()
            storitev = (
                s.query(Storitev)
                 .filter(Storitev.id_storitve == r.id_storitve)
                 .first()
                if r.id_storitve else None
            )

            ime_stranke = (
                f"{stranka.ime or ''} {stranka.priimek or ''}".strip()
                if stranka else "Neznana stranka"
            )
            ime_storitve = storitev.ime_storitve if storitev else "neznana storitev"
            datum_str = r.datum.strftime('%d.%m.%Y') if r.datum else '?'
            ura_str   = r.ura.strftime('%H:%M')    if r.ura   else '?'

            s.add(Sporocilo(
                id_stranke  = r.id_stranke,
                id_frizerja = frizer_id,
                naslov      = naslov,
                vsebina     = (
                    f"Stranka {ime_stranke} je preklicala rezervacijo za "
                    f"storitev '{ime_storitve}' dne {datum_str} ob {ura_str}."
                ),
                prebrano    = False,
            ))
        s.commit()

        return (
            s.query(Sporocilo)
             .filter(
                 Sporocilo.id_frizerja == frizer_id,
                 Sporocilo.prebrano == False,
                 Sporocilo.naslov.like('Preklic rezervacije%'),
             )
             .order_by(Sporocilo.datum.desc())
             .all()
        )
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def oznaci_prebrano(id_sporocila, frizer_id):
    """Označi obvestilo kot prebrano — le če pripada temu frizerju."""
    s = db.get_session()
    try:
        spr = (
            s.query(Sporocilo)
             .filter(
                 Sporocilo.id == id_sporocila,
                 Sporocilo.id_frizerja == frizer_id,
             )
             .first()
        )
        if not spr:
            return False
        spr.prebrano = True
        s.commit()
        return True
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()