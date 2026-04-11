import sys
import os
from flask import Flask

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index

f_app = Flask(__name__, template_folder='templates')


@f_app.get('/')
def home():
    return controllers.index.home()


@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()


@f_app.route('/salon')
def salon_pregled():
    return controllers.sv_salon.pregled()


@f_app.route('/salon/dodaj', methods=['GET', 'POST'])
def salon_dodaj():
    return controllers.sv_salon.dodaj_osebe()


@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
def salon_rezerviraj():
    return controllers.sv_salon.nova_rezervacija()


@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.sv_salon.saloni()


@f_app.route('/storitve', methods=['GET', 'POST'])
def storitve():
    return controllers.sv_salon.storitve()


@f_app.route('/urnik', methods=['GET', 'POST'])
def urnik():
    return controllers.sv_salon.urnik()


if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)
