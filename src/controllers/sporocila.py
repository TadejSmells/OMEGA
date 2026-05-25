from flask import render_template, redirect, url_for, session, request, flash, abort

import db
from models.models import Frizer
import models.model_sprocil as model_sprocil
import models.komentar_salona as komentar_salona


def _frizer_iz_seje():
    """Vrne id_frizer prijavljenega frizerja ali None."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    s = db.get_session()
    try:
        frizer = s.query(Frizer).filter(Frizer.user_id == user_id).first()
    finally:
        s.close()
    return frizer.id_frizer if frizer else None


def vsa_sporocila():
    """Prikaže vsa sporočila prijavljenega frizerja."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    s = db.get_session()
    try:
        frizer = s.query(Frizer).filter(Frizer.user_id == user_id).first()
    finally:
        s.close()

    if not frizer:
        return redirect(url_for('login'))

    sporocila = model_sprocil.seznam_sporocil(frizer.id_frizer)
    return render_template('sporocila.html', sporocila=sporocila)


def podrobnosti_sporocila(id):
    """Prikaže podrobnosti enega sporočila — le lastniku (frizerju) sporočila."""
    id_frizerja = _frizer_iz_seje()
    if id_frizerja is None:
        return redirect(url_for('login'))

    sporocilo = model_sprocil.podrobnosti_sporocila(id)
    if not sporocilo:
        return redirect(url_for('vsa_sporocila'))

    # Sporočilo mora pripadati prijavljenemu frizerju
    if sporocilo.id_frizerja != id_frizerja:
        abort(403)

    # Označi kot prebrano ob odprtju
    try:
        model_sprocil.oznaci_prebrano(id, id_frizerja)
    except Exception:
        pass

    return render_template('sporocila_tedaili.html', sporocilo=sporocilo)


# ── NOVO: STRANKA POŠLJE SPOROČILO FRIZERJU ──────────────────────────────────

def poslji_frizerju(id_frizerja):
    """
    Stranka pošlje sporočilo določenemu frizerju.
    Sproženo iz obrazca na profilu frizerja (POST /frizer/<id>/sporocilo).
    """
    db.validate_csrf()

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if session.get('role') != 'stranka':
        flash("Samo prijavljene stranke lahko pošljejo sporočilo frizerju.", "error")
        return redirect(url_for('frizer_profil', frizer_id=id_frizerja))

    id_stranke = komentar_salona.get_stranka_id(user_id)
    if not id_stranke:
        flash("Tvoj uporabniški račun ni povezan s stranko.", "error")
        return redirect(url_for('frizer_profil', frizer_id=id_frizerja))

    naslov = request.form.get('naslov', '')
    vsebina = request.form.get('vsebina', '')

    try:
        model_sprocil.poslji_sporocilo(id_stranke, id_frizerja, naslov, vsebina)
        flash("Sporočilo je bilo poslano.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception:
        flash("Napaka pri pošiljanju sporočila. Poskusi znova.", "error")

    return redirect(url_for('frizer_profil', frizer_id=id_frizerja))
