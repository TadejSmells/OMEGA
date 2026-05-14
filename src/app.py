import sys
import os
from flask import Flask, redirect
from db import login_required, admin_required, frizer_required, generate_csrf_token

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index
import controllers.auth
import controllers.rezervacije
import controllers.storitve
import controllers.ab_rezervacije
import controllers.faq
import controllers.saloni_controller
import controllers.uredi_rezervacijo
import controllers.kontakt_stranka_controller
import controllers.rezervacije_stranke_controller
import controllers.frizer_controller
import controllers.blokade_controller
import controllers.moje_rezervacije_controller
import controllers.pirkaz_stranke
import controllers.preklic_rezervacije_controller
import controllers.sporocila
import controllers.oznacevanje_priljubljenih_storitev
import controllers.komentar_salona
import controllers.priljubljeni_saloni
import controllers.prosti_termini_controller

f_app = Flask(__name__, template_folder='templates')
f_app.secret_key = os.environ.get('SECRET_KEY', 'pls spremeni')
f_app.jinja_env.globals['csrf_token'] = generate_csrf_token

# ── INDEX ─────────────────────────────────────────────────────────────────────
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
#───────────────────────začetni routi, PUSTI PRI MIRU────────────────────────────


# ─────────────────────────────────AUTH───────────────────────────────────────
@f_app.route('/salon/dodaj', methods=['GET', 'POST'])
def salon_dodaj():
    return controllers.sv_salon.dodaj_osebe()


@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
def salon_rezerviraj():
    return controllers.sv_salon.nova_rezervacija()


@f_app.route('/vsi_saloni', methods=['GET', 'POST'])
def vsi_saloni():
    return controllers.sv_salon.saloni()


@f_app.route('/storitve', methods=['GET', 'POST'])
def storitve():
    return controllers.sv_salon.storitve()


# ── AUTH ──────────────────────────────────────────────────────────────────────
@f_app.route("/register", methods=["GET", "POST"])
def register():
    return controllers.auth.register()

@f_app.route("/login", methods=["GET", "POST"])
def login():
    return controllers.auth.login()

@f_app.get('/logout')
def logout():
    return controllers.auth.logout()

@f_app.get('/profil')
def profil():
    return controllers.auth.profil()

@f_app.route('/salon/<int:salon_id>/termini')
def salon_termini_view(salon_id):
    return controllers.prosti_termini_controller.prikazi_termine_za_salon(salon_id)
# ── SALONI ────────────────────────────────────────────────────────────────────
@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.saloni_controller.saloni()

@f_app.get('/seznam_salonov')
def seznam_salonov_alias():
    return controllers.sv_salon.saloni()

@f_app.route('/salon/<int:salon_id>')
def salon_detail(salon_id):
    return controllers.sv_salon.salon_detail(salon_id)

@f_app.route('/salon')
def salon_pregled():
    return controllers.sv_salon.pregled()

@f_app.route("/saloni_view")
def saloni_view():
    return controllers.sv_salon.saloni_view()

@f_app.route('/salon/<int:salon_id>/komentar', methods=['POST'])
@login_required
def salon_komentar(salon_id):
    return controllers.komentar_salona.dodaj_komentar_salonu(salon_id)

# ── REZERVACIJE ───────────────────────────────────────────────────────────────
@f_app.route('/rezervacije', methods=['GET', 'POST'])
@login_required
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()

@f_app.route('/rezervacije/izbrisi/<int:id_rezervacije>', methods=['POST'])
@login_required
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)

@f_app.route('/rezervacije/preklic/<int:id_rezervacije>', methods=['POST'])
@login_required
def rezervacije_preklic(id_rezervacije):
    return controllers.rezervacije.preklici_rezervacijo(id_rezervacije)



@f_app.get('/vse_rezervacije')
@login_required
def vse_rezervacije():
    return controllers.ab_rezervacije.pregled_rezervacij()

@f_app.route('/zgodovina')
@login_required
def zgodovina():
    return controllers.sv_salon.zgodovina()

@f_app.route('/rezervacije/uredi/<int:id_rezervacije>', methods=['GET', 'POST'])
@login_required
def uredi_rezervacijo(id_rezervacije):
    return controllers.uredi_rezervacijo.uredi_rezervacijo(id_rezervacije)

@f_app.route('/prosti_termini')
def prosti_termini():
    return controllers.sv_salon.prosti_termini()
@f_app.route('/blokade', methods=['GET', 'POST'])
@frizer_required
def blokade():
    return controllers.blokade_controller.blokade()

@f_app.route('/moje')
@login_required
def moje():
    return controllers.moje_rezervacije_controller.moje_rezervacije()

@f_app.route('/moje/uredi/<int:id_rezervacije>', methods=['GET', 'POST'])
@login_required
def uredi_mojo(id_rezervacije):
    return controllers.moje_rezervacije_controller.uredi_mojo_rezervacijo(id_rezervacije)

@f_app.route('/moje/preklic/<int:id_rezervacije>', methods=['POST'])
@login_required
def preklic_moje(id_rezervacije):
    return controllers.moje_rezervacije_controller.preklic_moje_rezervacije(id_rezervacije)

# ── STORITVE ──────────────────────────────────────────────────────────────────
@f_app.route('/cenik')
def cenik():
    return controllers.storitve.pridobi_storitve()

@f_app.route('/vse_storitve')
def seznam_storitev():
    return controllers.storitve.pridobi_storitve()

@f_app.get('/seznam_storitev')
def seznam_storitev_alias():
    return controllers.storitve.pridobi_storitve()

@f_app.route('/storitve/dodaj', methods=['GET', 'POST'])
@admin_required
def dodaj_storitev():
    return controllers.storitve.dodaj_storitev()

@f_app.route('/storitve/priljubljena/<int:id_storitve>', methods=['POST'])
@login_required
def priljubljena_storitev(id_storitve):
    return controllers.oznacevanje_priljubljenih_storitev.toggle_priljubljeno(id_storitve)

@f_app.route('/storitve/priljubljene')
@login_required
def moje_priljubljene_storitve():
    return controllers.oznacevanje_priljubljenih_storitev.moje_priljubljene()


# ── OSTALO ────────────────────────────────────────────────────────────────────
@f_app.route('/stranke_uredi', methods=['GET', 'POST'])
@login_required
def stranke():
    return controllers.pirkaz_stranke.seznam_stranke()

@f_app.route('/stranke_uredi/shrani', methods=['POST'])
@login_required
def stranke_shrani():
    return controllers.pirkaz_stranke.shrani_stranko()

@f_app.route('/stranke_uredi/izbrisi', methods=['POST'])
@login_required
def izbrisi_stranko():
    return controllers.pirkaz_stranke.izbrisi_stranko()

@f_app.route('/urnik', methods=['GET', 'POST'])
@login_required
def urnik():
    return controllers.sv_salon.urnik()

@f_app.route('/faq', methods=['GET', 'POST'])
def faq():
    return controllers.faq.faq()

@f_app.route("/admin")
@admin_required
def admin():
    return controllers.sv_setup.admin()

@f_app.route("/frizer")
@frizer_required
def frizer():
    return controllers.preklic_rezervacije_controller.frizer_panel()

@f_app.route("/frizer/preklic/<int:id_rezervacije>", methods=["POST"])
@frizer_required
def frizer_preklic_rezervacije(id_rezervacije):
    return controllers.preklic_rezervacije_controller.preklic_rezervacije(id_rezervacije)
@f_app.route("/stranka")
@login_required
def stranka():
    return controllers.storitve.stranka()

@f_app.route('/kontakti_strank')
@login_required
def kontakti_strank():
   return controllers.kontakt_stranka_controller.kontakti_mojih_strank()
@f_app.route('/rezervacije_stranke')
@login_required
def rezervacije_stranke():
    return controllers.rezervacije_stranke_controller.moje_rezervacije()

@f_app.route('/frizerji')
def seznam_frizerjev():
    return controllers.frizer_controller.seznam_frizerjev()
 
@f_app.route('/frizer/<int:frizer_id>')
def frizer_profil(frizer_id):
    return controllers.frizer_controller.frizer_profil(frizer_id)

@f_app.route('/frizerji/dodaj', methods=['GET', 'POST'])
@admin_required
def dodaj_frizer():
    return controllers.frizer_controller.dodaj_frizer()

@f_app.route("/sporocila")
def vsa_sporocila():
    return controllers.sporocila.vsa_sporocila()

@f_app.route("/sporocilo/<int:id>")
def sporocilo_detail(id):
    return controllers.sporocila.podrobnosti_sporocila(id)
# ── ROUTI ZA VAŠE FUNKCIJE, DODAJTE TUKAJ ────────────────────────────────────
#@f_app.route('/"tvoja_pot"')
#def "tvoja_pot"():
#    return controllers.ime_controllerja.funkcija()
@f_app.route('/salon/<int:salon_id>/favorite', methods=['POST'])
def toggle_favorite(salon_id):
    return controllers.priljubljeni_saloni.toggle_favorite(salon_id)
if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)