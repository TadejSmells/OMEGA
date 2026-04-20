#tuki notri je kako mora zgledat controller, da se lahko uporablja v app.py
from flask import render_template
from models import model_primer_modela
#v primeru poizvedbe da nekaj naredimo, npr. pridobimo podatke iz baze, jih obdelamo in jih posredujemo v template¸


def funkcija():

    return render_template(
        "primer_template.html",
        podatki = model_primer_modela.get_vse_podatke()
    )

#ta file dela, da lahko v app.py kličemo funkcijo funkcija() in nam vrne render_template, 
# ki nam prikaže template in podatke iz baze, 
# ki jih pridobimo z modelom model_primer_modela.get_vse_podatke()