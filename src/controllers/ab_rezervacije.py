from flask import render_template, request, redirect
from models import model_rezervacije


def pregled_rezervacij():
    from flask import session

    vloga = session.get('role')
    frizer_id = session.get('user_id')

    if vloga == 'frizer':
        rezervacije = model_rezervacije.get_rezervacije_za_frizerja(frizer_id)
    else:
        rezervacije = model_rezervacije.get_vse_rezervacije()

    skupaj = len(rezervacije)
    aktivnih = sum(1 for r in rezervacije if r[8] == 'active')
    preklicanih = sum(1 for r in rezervacije if r[8] == 'cancelled')

    return render_template(
        "vse_rezervacije.html",
        rezervacije=rezervacije,
        skupaj=skupaj,
        aktivnih=aktivnih,
        preklicanih=preklicanih,
        je_frizer=(vloga == 'frizer'),
    )




def preklic_rezervacije(id_rezervacije):
    path = request.args.get('path', '/vse_rezervacije')
    model_rezervacije.preklic_rezervacije(id_rezervacije)
    return redirect(path)