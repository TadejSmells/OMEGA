from flask import render_template, request, redirect, url_for
from models import model_stranke


def seznam_stranke():
    stranke = model_stranke.get_vse_stranke()
    izbrana = None

    if request.method == 'POST':
        stranka_id = request.form.get('stranka_id')
        if stranka_id:
            izbrana = model_stranke.get_stranko(int(stranka_id))

    return render_template("seznam_stranke.html", stranke=stranke, izbrana=izbrana)


def shrani_stranko():
    id_stranke = int(request.form.get('id_stranke'))
    ime = request.form.get('ime')
    priimek = request.form.get('priimek')
    mail = request.form.get('mail')
    telefon = request.form.get('telefon')
    id_naj_frizer = request.form.get('id_naj_frizer') or None

    model_stranke.uredi_stranko(id_stranke, ime, priimek, mail, telefon, id_naj_frizer)

    return redirect(url_for('stranke'))