import sys
import os
from flask import Flask, redirect

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index
import controllers.auth
import controllers.rezervacije
import controllers.storitve
import controllers.ab_rezervacije
import controllers.faq 
#import controllers.primer_controller

f_app = Flask(__name__, template_folder='templates')

# ───────────────────────začetni routi, PUSTI PRI MIRU────────────────────────
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
# ───────────────────────začetni routi, PUSTI PRI MIRU────────────────────────

# ─────────────────────────────────AUTH───────────────────────────────────────
@f_app.route("/register", methods=["GET", "POST"])
def register():
    return controllers.auth.register()

@f_app.route("/login", methods=["GET", "POST"])
def login():
    return controllers.auth.login()

@f_app.get('/profil')
def profil():
    return controllers.auth.profil()
# ─────────────────────────────────AUTH───────────────────────────────────────

# ─────────────────────────────────SALONI─────────────────────────────────────
@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.sv_salon.saloni()

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
# ─────────────────────────────────SALONI─────────────────────────────────────

# ─────────────────────────────────REZERVACIJE─────────────────────────────────
@f_app.route('/rezervacije', methods=['GET', 'POST'])
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()

@f_app.route('/rezervacije/izbrisi/<int:id_rezervacije>', methods=['POST'])
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)

@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
def salon_rezerviraj_old():
    return redirect('/rezervacije')

@f_app.get('/vse_rezervacije')
def vse_rezervacije():
    return controllers.ab_rezervacije.pregled_rezervacij()

@f_app.route('/zgodovina')
def zgodovina():
    return controllers.sv_salon.zgodovina()
# ─────────────────────────────────REZERVACIJE─────────────────────────────────

# ─────────────────────────────────STORITVE────────────────────────────────────
@f_app.route('/cenik')
def cenik():
    return controllers.storitve.pridobi_storitve()

@f_app.route('/storitve')
def seznam_storitev():
    return controllers.storitve.pridobi_storitve()

@f_app.get('/seznam_storitev')
def seznam_storitev_alias():
    return controllers.storitve.pridobi_storitve()
# ─────────────────────────────────STORITVE────────────────────────────────────

# ─────────────────────────────────OSTALO──────────────────────────────────────
@f_app.route('/stranke')
def stranke():
    return controllers.sv_salon.seznam_stranke()

@f_app.route('/urnik', methods=['GET', 'POST'])
def urnik():
    return controllers.sv_salon.urnik()

@f_app.route('/faq', methods=['GET', 'POST'])
def faq():
    return controllers.faq.faq()


# ──────────────ROUTI ZA VAŠE FUNKCIJE, DODAJTE TUKAJ──────────────────────────
#@f_app.route('/"tvoja_pot"')
#def "tvoja_pot"():
#    return controllers.ime_controllerja.funkcija()

# ─────────────────────────────────KAR JE SPODAJ PUSTI PRI MIRU───────────────
if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)