import os
import sys

from flask import Flask

from db import login_required, admin_required, frizer_required, generate_csrf_token

# Controllers live under src/, so extend sys.path BEFORE importing them
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.ab_rezervacije
import controllers.auth
import controllers.blokade_controller
import controllers.faq
import controllers.frizer_controller
import controllers.index
import controllers.con_komentar_salona
import controllers.komentar_frizer
import controllers.kontakt_stranka_controller
import controllers.moje_rezervacije_controller
import controllers.obvestila_frizer_controller
import controllers.oznacevanje_priljubljenih_storitev
import controllers.pirkaz_stranke
import controllers.preklic_rezervacije_controller
import controllers.priljubljene_storitve
import controllers.priljubljeni_saloni_controller
import controllers.prosti_termini_controller
import controllers.rezervacije
import controllers.rezervacije_stranke_controller
import controllers.salon_controller
import controllers.saloni_controller
import controllers.sporocila
import controllers.storitve
import controllers.storitev_detail_controller
import controllers.sv_salon
import controllers.sv_setup
import controllers.uredi_rezervacijo
import controllers.uredi_salon_controller
import controllers.con_salon_detail
import controllers.uredi_storitev_controller

f_app = Flask(__name__, template_folder='templates')
f_app.secret_key = os.environ.get('SECRET_KEY', 'pls spremeni')
f_app.jinja_env.globals['csrf_token'] = generate_csrf_token
f_app.jinja_env.globals['get_obvestila_frizer'] = (
    controllers.obvestila_frizer_controller.obvestila_za_frizerja
)
from flask import Flask, redirect, request, session
from flask import session as _session
from models import model_rezervacije_stranke as _mrs

@f_app.context_processor
def inject_global_notifications():
    preklicane = []
    if _session.get('user_id') and _session.get('role') == 'stranka':
        try:
            vse = _mrs.get_preklicane_rezervacije_uporabnika(_session['user_id'])
            videne = _session.get('videne_preklicane', [])
            # r[0] = id_rezervacije (confirmed from model_obvestilo_preklic.py)
            preklicane = [r for r in vse if r[0] not in videne]
        except Exception:
            preklicane = []
    return dict(preklicane_rezervacije=preklicane)

@f_app.post('/opomnik/opusti')
@login_required
def opusti_opomnik():
    from flask import session
    session.pop('opomnik_rezervacije', None)
    session.pop('opomnik_tip', None)
    from flask import request as _req
    return redirect(_req.referrer or '/')

# PREKLICANE REZERVACIJE DISMISS (session-based tracking)
@f_app.post('/preklicana/opusti/<int:id_rez>')
@login_required
def opusti_preklicano(id_rez):
    from flask import session, request as _req
    videne = session.get('videne_preklicane', [])
    if id_rez not in videne:
        videne.append(id_rez)
    session['videne_preklicane'] = videne
    return redirect(_req.referrer or '/')
# INDEX & SETUP — PUSTI PRI MIRU

@f_app.get('/')
def home():
    return controllers.index.home()

@f_app.get('/zacetna_stran')
def zacetna_stran_alias():
    return controllers.index.home()

@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()

@f_app.get('/polni_db')
def polni_db():
    return controllers.sv_setup.polni_db()

# AUTH

@f_app.route('/register', methods=['GET', 'POST'])
def register():
    return controllers.auth.register()

@f_app.route('/login', methods=['GET', 'POST'])
def login():
    return controllers.auth.login()

@f_app.get('/logout')
def logout():
    return controllers.auth.logout()

@f_app.get('/profil')
def profil():
    return controllers.auth.profil()

# SALONI

@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.saloni_controller.saloni()

@f_app.get('/salon')
def salon_pregled():
    return controllers.sv_salon.pregled()

@f_app.get('/salon/<int:salon_id>')
def salon_detail(salon_id):
    return controllers.con_salon_detail.salon_detail(salon_id)

@f_app.get('/salon/<int:salon_id>/termini')
def salon_termini_view(salon_id):
    return controllers.prosti_termini_controller.prikazi_termine_za_salon(salon_id)

@f_app.post('/salon/<int:salon_id>/komentar')
@login_required
def salon_komentar(salon_id):
    return controllers.con_komentar_salona.dodaj_komentar_salonu(salon_id)

@f_app.post('/frizer/<int:frizer_id>/komentar')
@login_required
def frizer_komentar(frizer_id):
    return controllers.komentar_frizer.dodaj(frizer_id)

@f_app.post('/salon/<int:salon_id>/favorite')
def toggle_favorite(salon_id):
    return controllers.priljubljeni_saloni_controller.toggle_favorite(salon_id)

@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
@login_required
def salon_rezerviraj():
    return controllers.rezervacije.nova_rezervacija()

@f_app.route('/saloni/dodaj', methods=['GET', 'POST'])
@admin_required
def dodaj_salon():
    return controllers.salon_controller.dodaj_salon()

@f_app.get('/prosti_termini')
def prosti_termini():
    return controllers.sv_salon.prosti_termini()

@f_app.get('/priljubljeni_saloni')
@login_required
def priljubljeni_saloni():
    return controllers.priljubljeni_saloni_controller.prikazi()

@f_app.route('/saloni/uredi/<int:salon_id>', methods=['GET', 'POST'])
@admin_required
def saloni_uredi(salon_id):
    return controllers.uredi_salon_controller.uredi_salon(salon_id)

# FRIZERJI 

@f_app.get('/frizerji')
def seznam_frizerjev():
    return controllers.frizer_controller.seznam_frizerjev()

@f_app.get('/frizerji/lokacije')
def frizerji_na_lokaciji():
    return controllers.frizer_controller.frizerji_na_lokaciji()

@f_app.get('/frizer/<int:frizer_id>')
def frizer_profil(frizer_id):
    return controllers.frizer_controller.frizer_profil(frizer_id)

@f_app.route('/frizerji/dodaj', methods=['GET', 'POST'])
@admin_required
def dodaj_frizer():
    return controllers.frizer_controller.dodaj_frizer()

# STORITVE

@f_app.route('/storitve', methods=['GET', 'POST'])
def storitve():
    return controllers.storitve.pridobi_storitve()

@f_app.get('/cenik')
def cenik():
    return controllers.storitve.pridobi_storitve()

@f_app.get('/vse_storitve')
def seznam_storitev():
    return controllers.storitve.pridobi_storitve()

@f_app.get('/seznam_storitev')
def seznam_storitev_alias():
    return controllers.storitve.pridobi_storitve()

@f_app.route('/storitve/dodaj', methods=['GET', 'POST'])
@admin_required
def dodaj_storitev():
    return controllers.storitve.dodaj_storitev()

@f_app.post('/storitve/priljubljena/<int:id_storitve>')
@login_required
def priljubljena_storitev(id_storitve):
    return controllers.oznacevanje_priljubljenih_storitev.toggle_priljubljeno(id_storitve)

@f_app.get('/storitve/priljubljene')
@login_required
def moje_priljubljene_storitve():
    return controllers.priljubljene_storitve.prikazi()


@f_app.route('/storitve/uredi/<int:storitev_id>', methods=['GET', 'POST'])
@admin_required
def uredi_storitev(storitev_id):
    return controllers.uredi_storitev_controller.uredi_storitev(storitev_id)

@f_app.get('/storitev/<int:storitev_id>')
def storitev_detail(storitev_id):
    return controllers.storitev_detail_controller.storitev_detail(storitev_id)

@f_app.post('/storitev/<int:storitev_id>/komentar')
@login_required
def storitev_komentar(storitev_id):
    return controllers.storitev_detail_controller.dodaj_komentar_storitvi(storitev_id)
# REZERVACIJE

@f_app.route('/rezervacije', methods=['GET', 'POST'])
@login_required
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()

@f_app.post('/rezervacije/izbrisi/<int:id_rezervacije>')
@login_required
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)

@f_app.post('/rezervacije/preklic/<int:id_rezervacije>')
@login_required
def rezervacije_preklic(id_rezervacije):
    return controllers.rezervacije.preklici_rezervacijo(id_rezervacije)

@f_app.route('/rezervacije/uredi/<int:id_rezervacije>', methods=['GET', 'POST'])
@login_required
def uredi_rezervacijo(id_rezervacije):
    return controllers.uredi_rezervacijo.uredi_rezervacijo(id_rezervacije)

@f_app.get('/vse_rezervacije')
@login_required
def vse_rezervacije():
    return controllers.ab_rezervacije.pregled_rezervacij()

@f_app.get('/zgodovina')
@login_required
def zgodovina():
    return controllers.sv_salon.zgodovina()

# MOJE REZERVACIJE

@f_app.get('/moje')
@login_required
def moje():
    return controllers.moje_rezervacije_controller.moje_rezervacije()

@f_app.route('/moje/uredi/<int:id_rezervacije>', methods=['GET', 'POST'])
@login_required
def uredi_mojo(id_rezervacije):
    return controllers.moje_rezervacije_controller.uredi_mojo_rezervacijo(id_rezervacije)

@f_app.post('/moje/preklic/<int:id_rezervacije>')
@login_required
def preklic_moje(id_rezervacije):
    return controllers.moje_rezervacije_controller.preklic_moje_rezervacije(id_rezervacije)

# STRANKE

@f_app.route('/stranke_uredi', methods=['GET', 'POST'])
@login_required
def stranke():
    return controllers.pirkaz_stranke.seznam_stranke()

@f_app.post('/stranke_uredi/shrani')
@login_required
def stranke_shrani():
    return controllers.pirkaz_stranke.shrani_stranko()

@f_app.post('/stranke_uredi/izbrisi')
@login_required
def izbrisi_stranko():
    return controllers.pirkaz_stranke.izbrisi_stranko()

@f_app.get('/stranka')
@login_required
def stranka():
    return controllers.storitve.stranka()

@f_app.get('/kontakti_strank')
@login_required
def kontakti_strank():
    return controllers.kontakt_stranka_controller.kontakti_mojih_strank()

@f_app.get('/kontakti_strank/<int:id_stranke>')
@login_required
def kontakt_posamezne_stranke(id_stranke):
    return controllers.kontakt_stranka_controller.kontakt_posamezne_stranke(id_stranke)

@f_app.get('/rezervacije_stranke')
@login_required
def rezervacije_stranke():
    return controllers.rezervacije_stranke_controller.moje_rezervacije()

# FRIZER PANEL

@f_app.get('/frizer')
@frizer_required
def frizer():
    return controllers.sv_setup.frizer()

@f_app.post('/frizer/preklic/<int:id_rezervacije>')
@frizer_required
def frizer_preklic_rezervacije(id_rezervacije):
    return controllers.preklic_rezervacije_controller.preklic_rezervacije(id_rezervacije)

@f_app.post('/frizer/obvestilo/opusti/<int:id_sporocila>')
@frizer_required
def frizer_opusti_obvestilo(id_sporocila):
    return controllers.obvestila_frizer_controller.opusti_obvestilo(id_sporocila)

@f_app.route('/blokade', methods=['GET', 'POST'])
@frizer_required
def blokade():
    return controllers.blokade_controller.blokade()

# SPOROČILA

@f_app.get('/sporocila')
def vsa_sporocila():
    return controllers.sporocila.vsa_sporocila()

@f_app.get('/sporocilo/<int:id>')
def sporocilo_detail(id):
    return controllers.sporocila.podrobnosti_sporocila(id)

# ADMIN

@f_app.get('/admin')
@admin_required
def admin():
    return controllers.sv_setup.admin()

# OSTALO

@f_app.route('/urnik', methods=['GET', 'POST'])
@admin_required
def urnik():
    return controllers.sv_salon.urnik()

@f_app.route('/faq', methods=['GET', 'POST'])
def faq():
    return controllers.faq.faq()

if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)