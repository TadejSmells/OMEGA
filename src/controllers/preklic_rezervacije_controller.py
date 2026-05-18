from datetime import datetime, date, time, timedelta
from flask import render_template, redirect, flash, session
from models import model_preklic_rezervacije as model
import db


def _get_frizer_id():
    """Pomožna: vrne id_frizer iz tabele frizer za prijavljenega userja."""
    user_id = session.get('user_id')
    db_session = db.get_session()
    try:
        from models.models import Frizer
        frizer = db_session.query(Frizer).filter(Frizer.user_id == user_id).first()
        return frizer.id_frizer if frizer else None
    finally:
        db_session.close()


def frizer_panel():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") not in ("frizer", "admin"):
        return "Nimaš dostopa.", 403

    frizer_id = _get_frizer_id()
    vse = model.get_rezervacije_frizerja(frizer_id) if frizer_id else []

    danes = date.today()
    danes_str = str(danes)
    zacetek_tedna = danes - timedelta(days=danes.weekday())
    konec_tedna = zacetek_tedna + timedelta(days=6)

    rezervacije = []
    for r in vse:
        try:
            datum_r = date.fromisoformat(str(r[5]))
            if zacetek_tedna <= datum_r <= konec_tedna:
                rezervacije.append({
                    "id_rezervacije": r[0],
                    "stranka":        r[1] or "—",
                    "storitev":       r[2] or "—",
                    "salon":          r[3] or "—",
                    "datum":          str(r[4]) or "—",
                    "ura":            str(r[5]) or "—",
                    "status":         r[6] or "active",
                })
        except:
            pass

    naslednji_termin = None
    zdaj = datetime.now().time()
    danes_termini = [
        r for r in rezervacije
        if r["datum"] == danes_str and r["status"] != "cancelled"
    ]
    for t in sorted(danes_termini, key=lambda x: x["ura"]):
        try:
            if time.fromisoformat(str(t["ura"])[:5]) >= zdaj:
                naslednji_termin = t
                break
        except:
            pass

    stats = {
        "rezervacije_teden": len(rezervacije),
        "rezervacije_danes":  sum(1 for r in rezervacije if r["datum"] == danes_str),
        "prosti_termini":     "—",  # po potrebi povezi z urnik logiko
        "stranke_teden":      len(set(r["stranka"] for r in rezervacije if r["stranka"] != "—")),
        "opravljene":         sum(1 for r in vse if r[6] == "active"),
    }

    zadnja_aktivnost = []
    for r in vse[:5]:
        if r[6] == "cancelled":
            tip = "Rezervacija preklicana"
            dot = "rose"
        else:
            tip = "Nova rezervacija"
            dot = "brown"
        zadnja_aktivnost.append({
            "tip":   tip,
            "ime":   r[1] or "—",
            "datum": str(r[5]) or "—",
            "ura":   str(r[6]) or "—",
            "dot":   dot,
        })

    sporocila = []
    if hasattr(model, "get_sporocila_frizerja"):
        raw = model.get_sporocila_frizerja(frizer_id) or []
        for s in raw[:5]:
            sporocila.append({
                "stranka":  s[1] or "—",
                "vsebina":  s[2] or "",
                "datum":    s[3],
                "prebrano": bool(s[4]),
            })

    return render_template(
        "frizer.html",
        stats=stats,
        rezervacije=rezervacije,
        naslednji_termin=naslednji_termin,
        zadnja_aktivnost=zadnja_aktivnost,
        sporocila=sporocila,
        frizer_id=frizer_id,
    )


def preklic_rezervacije(id_rezervacije):
    """Prekliče rezervacijo — samo če pripada prijavljenemu frizerju."""
    frizer_id = _get_frizer_id()
    if frizer_id is None:
        flash("Frizerjev račun ni najden.", "error")
        return redirect('/frizer')

    uspeh = model.preklic_rezervacije_frizerja(id_rezervacije, frizer_id)
    if uspeh:
        flash("Rezervacija je bila preklicana.", "success")
    else:
        flash("Rezervacija ni bila najdena ali nimate dovoljenja.", "error")
    return redirect('/frizer')
