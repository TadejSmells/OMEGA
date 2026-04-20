from flask import render_template, request, redirect
from models import model_salon



#tukaj se bodo funkcije odstranile
#za vsak user sotry se naredi posebi datotekoo v mapi controllers, kjer se definira funkcijo.


def pregled():
    return render_template("sv_pregled.html",
                           frizerji=model_salon.get_vse('frizer'),
                           stranke=model_salon.get_vse('stranka'),
                           rezervacije=model_salon.get_vse('rezervacija'),
                           saloni=model_salon.get_vse('salon'),
                           storitve=model_salon.get_vse('storitev'),
                           urnik=model_salon.get_vse('urnik'))

#naredi novo datoteko pirkaz_stranke.py in controllers, kjer se definira funkcija prikaz_stranke, ki bo prikazala seznam strank
def seznam_stranke():
    stranke = model_salon.get_vse('stranka')
    return render_template("seznam_stranke.html", stranke=stranke)


def storitve():
    if request.method == 'POST':
        model_salon.dodaj_storitev(
            request.form.get('ime_storitve'),
            request.form.get('cena'),
            request.form.get('trajanje')
        )
        return redirect('/storitve')
    return render_template("storitve.html", storitve=model_salon.get_vse('storitev'))


#premakne v datoteko salon_info.py
def saloni_view_info():
    return render_template(
        "saloni_info.html",
        saloni=model_salon.get_vse('salon')
    )
