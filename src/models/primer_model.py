#tukaj notri je primer modela

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
#importamo db, da lahko delamo z bazo, 
# v tem primeru bomo delali z modelom model_primer_modela, 
# ki bo imel funkcijo get_vse_podatke(), 
# ki bo vrnila vse podatke iz baze, 
# ki jih bomo potem uporabili v controllerju

def get_vse_podatke():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tabela")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#ta funkcija get_vse_podatke() se poveže z bazo, izvede poizvedbo, da dobi vse podatke iz tabele,
# zapre povezavo in vrne podatke, ki jih potem lahko uporabimo v controllerju, da jih posredujemo v template in jih prikažemo uporabniku