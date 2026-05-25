from flask import request, session, redirect, url_for, flash
from models.model_uredi_profil import uredi_stranko, uredi_frizerja

def uredi_profil():
    if not session.get('user_id'):
        return redirect(url_for('profil'))

    user_id = session['user_id']
    role    = session.get('role')

    nov_username = request.form.get('username', '').strip()

    if role == 'stranka':
        ime     = request.form.get('ime', '').strip()
        priimek = request.form.get('priimek', '').strip()
        mail    = request.form.get('mail', '').strip()
        telefon = request.form.get('telefon', '').strip()

        if not all([nov_username, ime, priimek, mail, telefon]):
            flash("Vsa polja so obvezna.", "error")
            return redirect(url_for('profil'))

        ok, msg = uredi_stranko(user_id, ime, priimek, mail, telefon)

    elif role == 'frizer':
        ime     = request.form.get('ime', '').strip()
        kontakt = request.form.get('kontakt', '').strip()

        if not all([nov_username, ime, kontakt]):
            flash("Vsa polja so obvezna.", "error")
            return redirect(url_for('profil'))

        ok, msg = uredi_frizerja(user_id, ime, kontakt)

    else:
        flash("Nimate dovoljenja.", "error")
        return redirect(url_for('profil'))

    if ok:
        session['username'] = nov_username
        flash(msg, "success")
    else:
        flash(msg, "error")

    return redirect(url_for('profil'))