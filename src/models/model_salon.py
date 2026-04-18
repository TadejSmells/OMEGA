import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db

# ── DB SETUP ────────────────────────────────────────────────────────────────────

def setup_db():
    conn = db.get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    sql_path = os.path.join(os.path.dirname(__file__), '..', 'creation.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    conn.autocommit = False


    cursor.execute("SELECT COUNT(*) FROM salon")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO salon (ime, naslov, mesto, telefon) VALUES (%s, %s, %s, %s)",
                       ('Salon Lepote', 'Glavna ulica 1', 'Ljubljana', '01-123-456'))
        cursor.execute("INSERT INTO salon (ime, naslov, mesto, telefon) VALUES (%s, %s, %s, %s)",
                       ('Frizerski Studio', 'Cesta 2', 'Maribor', '02-654-321'))
        cursor.execute("INSERT INTO salon (ime, naslov, mesto, telefon) VALUES (%s, %s, %s, %s)",
                       ('Salon Elegance', 'Ulica 3', 'Celje', '03-789-012'))
        

    cursor.execute("SELECT COUNT(*) FROM frizer")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO frizer (salon_id, ime, kontakt) VALUES (%s, %s, %s)",
                       (1, 'Ana Kovač', '031-555-666'))
        cursor.execute("INSERT INTO frizer (salon_id, ime, kontakt) VALUES (%s, %s, %s)",
                       (2, 'Tina Zupan', '041-777-888'))
        cursor.execute("INSERT INTO frizer (salon_id, ime, kontakt) VALUES (%s, %s, %s)",
                       (3, 'Miha Novak', '040-999-000'))

    cursor.execute("SELECT COUNT(*) FROM stranka")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO stranka (ime, priimek, mail, telefon) VALUES (%s, %s, %s, %s)",
                       ('Luka', 'Novak', 'luka@test.si', '031-999-888'))
        cursor.execute("INSERT INTO stranka (ime, priimek, mail, telefon) VALUES (%s, %s, %s, %s)",
                       ('Maja', 'Kralj', 'maja@test.si', '031-111-222'))


    cursor.execute("SELECT COUNT(*) FROM storitev")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO storitev (ime_storitve, cena, trajanje) VALUES (%s, %s, %s)",
                       ('Upravljanje s kosmetskimi izdelki', 50.0, '01:00:00'))
        cursor.execute("INSERT INTO storitev (ime_storitve, cena, trajanje) VALUES (%s, %s, %s)",
                       ('Barvanje las', 70.0, '01:30:00'))
        

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


# ── INSERTS ────────────────────────────────────────────────────────────────────
#vse to gre stran, posebi user storyji vsaka stvar
def dodaj_frizerja(ime, kontakt, salon_id=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO frizer (ime, kontakt, salon_id) VALUES (%s, %s, %s)",
        (ime, kontakt, salon_id or None)
    )
    conn.commit()
    cursor.close()
    conn.close()


def dodaj_stranko(ime, priimek, mail, telefon, id_naj_frizer=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stranka (ime, priimek, mail, telefon, id_naj_frizer) VALUES (%s, %s, %s, %s, %s)",
        (ime, priimek or '', mail, telefon, id_naj_frizer or None)
    )
    conn.commit()
    cursor.close()
    conn.close()


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


def dodaj_salon(ime, naslov, mesto, telefon):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO salon (ime, naslov, mesto, telefon) VALUES (%s, %s, %s, %s)",
        (ime, naslov, mesto, telefon)
    )
    conn.commit()
    cursor.close()
    conn.close()


def dodaj_storitev(ime_storitve, cena, trajanje):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO storitev (ime_storitve, cena, trajanje) VALUES (%s, %s, %s)",
        (ime_storitve, cena, trajanje)
    )
    conn.commit()
    cursor.close()
    conn.close()


def dodaj_urnik(frizer_id, dan, ura):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urnik (id_frizerja, dan, ura) VALUES (%s, %s, %s)",
        (frizer_id, dan, ura)
    )
    conn.commit()
    cursor.close()
    conn.close()
