import sys
import os
from flask import render_template, request, redirect, flash
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from models import model_faq
import db

def faq():
    if request.method == 'POST':
        db.validate_csrf()
 
        ime     = request.form.get('ime', '').strip()
        email   = request.form.get('email', '').strip()
        naslov  = request.form.get('tezava', '').strip()
        vsebina = request.form.get('opis', '').strip()
 
        if not ime or not email or not naslov or not vsebina:
            flash("Vsa polja so obvezna.", "error")
            return render_template('faq.html', faqi=model_faq.pridobi_faq())
 
        try:
            model_faq.postavi_sporocilo(ime=ime, email=email, naslov=naslov, vsebina=vsebina)
            flash("Sporočilo je bilo uspešno poslano! Kmalu vam bomo odgovorili.", "success")
        except Exception:
            flash("Napaka pri pošiljanju sporočila. Poskusite znova.", "error")
 
        return redirect('/faq')
 
    return render_template('faq.html', faqi=model_faq.pridobi_faq())