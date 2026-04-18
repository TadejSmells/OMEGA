from flask import render_template, request, redirect
from models import model_salon


def pregled():
    return render_template("sv_pregled.html",
                           frizerji=model_salon.get_vse('frizer'),
                           stranke=model_salon.get_vse('stranka'),
                           rezervacije=model_salon.get_vse('rezervacija'),
                           saloni=model_salon.get_vse('salon'),
                           storitve=model_salon.get_vse('storitev'),
                           urnik=model_salon.get_vse('urnik'))


def dodaj_osebe():
    if request.method == 'POST':
        tip = request.form.get('tip')
        ime = request.form.get('ime')
        if tip == 'frizer':
            model_salon.dodaj_frizerja(ime, request.form.get('kontakt'), request.form.get('salon_id'))
        else:
            model_salon.dodaj_stranko(ime, request.form.get('priimek'),
                                      request.form.get('mail'), request.form.get('telefon'),
                                      request.form.get('id_naj_frizer'))
        return redirect('/salon')
    frizerji = model_salon.get_vse('frizer')
    saloni = model_salon.get_vse('salon')
    return render_template("salon_dodaj.html", frizerji=frizerji, saloni=saloni)
    
def saloni():
    if request.method == 'POST':
        model_salon.dodaj_salon(
            request.form.get('ime'),
            request.form.get('naslov'),
            request.form.get('mesto'),
            request.form.get('telefon')
        )
        return redirect('/saloni')
    return render_template("saloni.html", saloni=model_salon.get_vse('salon'))


def storitve():
    if request.method == 'POST':
        model_salon.dodaj_storitev(
            request.form.get('ime_storitve'),
            request.form.get('cena'),
            request.form.get('trajanje')
        )
        return redirect('/storitve')
    return render_template("storitve.html", storitve=model_salon.get_vse('storitev'))


def urnik():
    if request.method == 'POST':
        model_salon.dodaj_urnik(
            request.form.get('frizer_id'),
            request.form.get('dan'),
            request.form.get('ura')
        )
        return redirect('/urnik')
    return render_template("urnik.html",
                           urnik=model_salon.get_vse('urnik'),
                           frizerji=model_salon.get_vse('frizer'))