from flask import render_template, request, redirect, abort
from models import model_salon



#tukaj se bodo funkcije odstranile
#za vsak user sotry se naredi posebi datotekoo v mapi controllers, kjer se definira funkcijo.


def pregled():
    return redirect('/saloni')

#naredi novo datoteko pirkaz_stranke.py in controllers, kjer se definira funkcija prikaz_stranke, ki bo prikazala seznam strank
def seznam_stranke():
    stranke = model_salon.get_vse('stranka')
    return render_template("seznam_stranke.html", stranke=stranke)

def saloni():
    try:
        saloni_list = model_salon.get_vse('salon')
    except Exception:
        saloni_list = []
    saloni_with_storitve = []
    
    for salon in saloni_list:
        salon_id = salon[0]
        try:
            storitve = model_salon.get_storitve_za_salon(salon_id)
        except Exception:
            storitve = []
        saloni_with_storitve.append({
            'salon': salon,
            'storitve': storitve
        })
    
    return render_template(
        "seznam_salonov.html",
        saloni=saloni_with_storitve
    )

def salon_detail(salon_id):
    try:
        salon = next((s for s in model_salon.get_vse('salon') if s[0] == salon_id), None)
    except Exception:
        salon = None

    if salon is None:
        abort(404)

    try:
        storitve = model_salon.get_storitve_za_salon(salon_id)
    except Exception:
        storitve = []

    return render_template(
        "salon.html",
        salon=salon,
        storitve=storitve,
        ocene=[]
    )

def storitve():
    if request.method == 'POST':
        model_salon.dodaj_storitev(
            request.form.get('ime_storitve'),
            request.form.get('cena'),
            request.form.get('trajanje')
        )
        return redirect('/storitve')
    return render_template("storitve.html", storitve=model_salon.get_vse('storitev'))


<<<<<<< HEAD
#premakne v datoteko salon_info.py
def saloni_view_info():
    return render_template(
        "saloni_view.html",
        saloni=model_salon.get_vse('salon')
    )

def saloni_view():
    return saloni_view_info()
=======
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

def zgodovina():
    rezervacije = model_salon.get_vse('rezervacija')
    return render_template("zgodovina.html", rezervacije=rezervacije)
>>>>>>> 5bc26f8 (Dodana zgodovina rezervacij)
