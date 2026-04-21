import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db

# ── DB SETUP ────────────────────────────────────────────────────────────────────
#ta del je potreben, ker se tuki ustvari baza sql in se napolni
#ostale stvari pod DB SETUP grejo ven, ker se bodo delale v user storyjih, 
# vsak user story bo imel svojo funkcijo za dodajanje podatkov
def setup_db():
    conn = db.get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    sql_path = os.path.join(os.path.dirname(__file__), '..', 'creation.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    conn.autocommit = False


   

def polni_db():
    conn = db.get_connection()
    conn.autocommit = False
    cursor = conn.cursor()

    sql_path = os.path.join(os.path.dirname(__file__), '..', 'testni_podatki.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()
    return True
# ── GETTERS ────────────────────────────────────────────────────────────────────

def get_vse(tip):
    conn = db.get_connection()
    cursor = conn.cursor()

    if tip == 'frizer':
        cursor.execute("SELECT id_frizer, salon_id, ime, kontakt FROM frizer ORDER BY id_frizer")
    elif tip == 'stranka':
        cursor.execute("SELECT id_stranke, ime, priimek, mail, telefon FROM stranka ORDER BY id_stranke")
    elif tip == 'rezervacija':
        cursor.execute("""
            SELECT r.id_rezervacije,
                   s.ime || ' ' || s.priimek,
                   f.ime,
                   sa.ime,
                   st.ime_storitve
            FROM rezervacija r
            LEFT JOIN stranka s ON r.id_stranke = s.id_stranke
            LEFT JOIN frizer f ON r.id_frizerja = f.id_frizer
            LEFT JOIN salon sa ON r.id_salona = sa.id
            LEFT JOIN storitev st ON r.id_storitve = st.id_storitve
            ORDER BY r.id_rezervacije
        """)
    elif tip == 'salon':
        cursor.execute("SELECT id, ime, naslov, mesto, telefon FROM salon ORDER BY id")
    elif tip == 'storitev':
        cursor.execute("SELECT id_storitve, ime_storitve, cena, trajanje FROM storitev ORDER BY id_storitve")
    elif tip == 'urnik':
        cursor.execute("""
            SELECT f.ime, u.dan, u.ura
            FROM urnik u
            LEFT JOIN frizer f ON u.id_frizerja = f.id_frizer
            ORDER BY u.dan, u.ura
        """)
    else:
        cursor.close()
        conn.close()
        return []

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_storitve_za_salon(salon_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT st.id_storitve, st.ime_storitve, st.cena, st.trajanje
        FROM storitev st
        INNER JOIN saloni_in_storitve sis ON st.id_storitve = sis.storitev_id
        WHERE sis.salon_id = %s
        ORDER BY st.ime_storitve
    """, (salon_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
# ── INSERTS ────────────────────────────────────────────────────────────────────
#vse to gre stran, posebi user storyji vsaka stvar

def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rezervacija (id_stranke, id_frizerja, id_salona, id_storitve) VALUES (%s, %s, %s, %s)",
        (stranka_id, frizer_id, salon_id or None, storitev_id or None)
    )
    conn.commit()
    cursor.close()
    conn.close()





