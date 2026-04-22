import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db

def get_vse_rezervacije():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT
                r.id_rezervacije,
                s.ime || ' ' || s.priimek  AS stranka,
                f.ime                       AS frizer,
                sa.ime                      AS salon,
                st.ime_storitve             AS storitev,
                st.cena                     AS cena,
                st.trajanje                 AS trajanje
            FROM rezervacija r
            LEFT JOIN stranka  s  ON r.id_stranke  = s.id_stranke
            LEFT JOIN frizer   f  ON r.id_frizerja = f.id_frizer
            LEFT JOIN salon    sa ON r.id_salona   = sa.id
            LEFT JOIN storitev st ON r.id_storitve = st.id_storitve
            ORDER BY r.id_rezervacije DESC
        """)
        return cursor.fetchall()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id):
    with db.get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO rezervacija (id_stranke, id_frizerja, id_salona, id_storitve)
               VALUES (%s, %s, %s, %s)""",
            (stranka_id, frizer_id, salon_id or None, storitev_id or None)
        )


def izbrisi_rezervacijo(id_rezervacije):
    with db.get_cursor() as cursor:
        cursor.execute(
            "DELETE FROM rezervacija WHERE id_rezervacije = %s",
            (id_rezervacije,)
        )