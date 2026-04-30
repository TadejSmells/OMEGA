# OMEGA — Management frizerskih salonov

> ⚠️ **PRED DELANJEM USER STORYJA SPOROČI VODJI TISTEGA DELA!**
> Za vse modele, controllerje in db.py kontaktiraj vodjo SQLAlchemy!
> Preden v app.py dodajaš funkcije, preveri če že obstajajo!

---

## Zahteve

Na računalniku mora biti nameščeno:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/)
- [Python 3.12+](https://www.python.org/downloads/)

---

## Zagon projekta

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/TadejSmells/OMEGA
cd OMEGA

# 2. Zaženi Docker
docker compose up --build

# 3. Odpri v brskalniku
http://localhost:8080/
```

**Ob prvem zagonu** klikni spodaj na domači strani:
- 🗄️ **Nastavi tabele baze** — zažene creation.sql
- 📦 **Naloži testne podatke** — zažene testni_podatki.sql

---

## Struktura projekta

```
src/
├── controllers/        ← Flask logika (en file per user story)
├── models/             ← SQLAlchemy funkcije za bazo (en file per user story)
│   ├── models.py       ← Definicije tabel — NE SPREMINJAJ
│   └── model_salon.py  ← Skupne funkcije + vzorec
├── templates/          ← HTML strani
├── app.py              ← Flask aplikacija + vsi routi
├── db.py               ← Povezava z bazo + varnostni dekoratorji
├── creation.sql        ← SQL za kreiranje tabel
└── testni_podatki.sql  ← Testni podatki
```

---

## Kako dodaš svoj user story

### Korak 1 — Model datoteka (`src/models/model_ime.py`)
```python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import TvojModel  # importaj tabelo iz models.py

def get_vse():
    db_session = db.get_session()
    try:
        rows = db_session.query(TvojModel).all()
        return [(r.id, r.ime) for r in rows]
    finally:
        db_session.close()
```

### Korak 2 — Controller datoteka (`src/controllers/ime.py`)
```python
from flask import render_template
from models import model_ime

def moja_funkcija():
    podatki = model_ime.get_vse()
    return render_template("moja_stran.html", podatki=podatki)
```

### Korak 3 — Dodaj v `app.py`
```python
# Na vrhu med importi:
import controllers.ime

# Med routami:
@f_app.route('/moja-pot')
@login_required  # dodaj če je stran zaščitena
def moja_pot():
    return controllers.ime.moja_funkcija()
```

### Korak 4 — HTML template (`src/templates/moja_stran.html`)
```html
{% extends "base.html" %}
{% block content %}
{% for p in podatki %}
    <p>{{ p[1] }}</p>
{% endfor %}
{% endblock %}
```

---

## Varnostni dekoratorji

Dostopni v `db.py` — dodaj nad route funkcijo v `app.py`:

| Dekorator | Kdo ima dostop |
|---|---|
| `@login_required` | vsi prijavljeni uporabniki |
| `@admin_required` | samo admin |
| `@frizer_required` | frizer in admin |

---

## Tabele v bazi

| Tabela | Opis |
|---|---|
| `salon` | Frizerski saloni |
| `frizer` | Frizerji (vezani na salon) |
| `stranka` | Stranke |
| `storitev` | Storitve in cenik |
| `saloni_in_storitve` | Katere storitve ponuja kateri salon |
| `urnik` | Delovni urnik frizerjev |
| `rezervacija` | Rezervacije (z datumom in uro) |
| `users` | Uporabniki (login, vloge: admin/frizer/stranka) |
| `faq` | Pogosta vprašanja |

---

## Vloge uporabnikov

| Vloga | Dostop po prijavi |
|---|---|
| `stranka` | Osnoven dostop, rezervacije |
| `frizer` | Frizer panel |
| `admin` | Admin panel, vse |

---

## Pogoste napake

| Napaka | Vzrok | Rešitev |
|---|---|---|
| `ModuleNotFoundError: No module named 'db'` | Manjka sys.path.append | Dodaj na vrh model datoteke |
| `ModuleNotFoundError: No module named 'controllers.xyz'` | Controller ne obstaja ali ni dodan v app.py | Ustvari datoteko in jo dodaj v app.py |
| `could not translate host name "db"` | Docker network problem | `docker compose down` nato `docker compose up --build` |
| Stran je prazna | Baza nima podatkov | Klikni 📦 Naloži testne podatke na domači strani |
| Port 5432 already allocated | Drug Docker container zaseda port | `docker compose down --remove-orphans` |