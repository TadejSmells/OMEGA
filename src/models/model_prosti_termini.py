import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from datetime import date, datetime, timedelta
from models.models import Frizer, Urnik, Rezervacija, BlokiranTermin


DNEVI_SL = ['PON', 'TOR', 'SRE', 'ČET', 'PET', 'SOB', 'NED']


def get_prosti_termini_po_dnevih(salon_id, dni_naprej=14, samo_frizer_id=None):
    """
    Vrne seznam dictov za naslednjih `dni_naprej` dni:
      {'datum': date, 'dan_ime': str, 'proste_ure': [(ura_str, frizer_ime, frizer_id), ...]}
    Slot je 'prost', če:
      - obstaja v urniku frizerja, ki pripada temu salonu
      - ni zaseden z aktivno rezervacijo
      - ne pade v noben blokiran interval
      - ni v preteklosti (samo za današnji dan)
    Opcionalno: samo_frizer_id omeji prikaz na enega frizerja.
    """
    s = db.get_session()
    try:
        danes = date.today()
        konec = danes + timedelta(days=dni_naprej - 1)
        zdaj  = datetime.now().time()

        # 1) Vsi termini iz urnika frizerjev tega salona v oknu
        q = (
            s.query(Urnik.id_frizerja, Urnik.dan, Urnik.ura, Frizer.ime)
            .join(Frizer, Urnik.id_frizerja == Frizer.id_frizer)
            .filter(Frizer.salon_id == salon_id)
            .filter(Urnik.dan >= danes)
            .filter(Urnik.dan <= konec)
        )
        if samo_frizer_id is not None:
            q = q.filter(Urnik.id_frizerja == samo_frizer_id)
        slots = q.all()

        if not slots:
            zasedeni = set()
            blokade_map = {}
        else:
            frizer_ids = {fid for fid, _, _, _ in slots}

            # 2) Zasedeni termini (aktivne rezervacije)
            zasedeni = set(
                s.query(Rezervacija.id_frizerja, Rezervacija.datum, Rezervacija.ura)
                .filter(Rezervacija.id_frizerja.in_(frizer_ids))
                .filter(Rezervacija.datum >= danes)
                .filter(Rezervacija.datum <= konec)
                .filter(Rezervacija.status == 'active')
                .all()
            )

            # 3) Blokirani intervali
            blokade = (
                s.query(BlokiranTermin.id_frizerja, BlokiranTermin.datum,
                        BlokiranTermin.ura_od, BlokiranTermin.ura_do)
                .filter(BlokiranTermin.id_frizerja.in_(frizer_ids))
                .filter(BlokiranTermin.datum >= danes)
                .filter(BlokiranTermin.datum <= konec)
                .all()
            )
            blokade_map = {}
            for fid, d, od, do in blokade:
                blokade_map.setdefault((fid, d), []).append((od, do))

        def je_blokiran(fid, d, ura):
            for od, do in blokade_map.get((fid, d), []):
                if od <= ura < do:
                    return True
            return False

        # 4) Filtriraj in grupiraj po datumih — tuple zdaj vsebuje tudi frizer_id
        po_dnevih = {}
        for fid, d, ura, ime in slots:
            if d == danes and ura < zdaj:
                continue
            if (fid, d, ura) in zasedeni:
                continue
            if je_blokiran(fid, d, ura):
                continue
            po_dnevih.setdefault(d, []).append((ura, ime, fid))

        # 5) Zaporedni dnevi (tudi prazni)
        rezultat = []
        for i in range(dni_naprej):
            d = danes + timedelta(days=i)
            proste = sorted(po_dnevih.get(d, []), key=lambda x: x[0])
            rezultat.append({
                'datum':      d,
                'dan_ime':    DNEVI_SL[d.weekday()],
                'proste_ure': [(u.strftime('%H:%M'), ime, fid) for u, ime, fid in proste],
            })
        return rezultat
    finally:
        s.close()


def najdi_najhitrejsi_index(dnevi):
    """Indeks prvega dneva, ki ima vsaj eno prosto uro. None, če ga ni."""
    for i, d in enumerate(dnevi):
        if d['proste_ure']:
            return i
    return None