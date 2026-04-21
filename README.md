# OMEGA — Management frizerskih salonov

Repozitorij za skupino Omega. Projekt omogoča upravljanje frizerskih salonov: rezervacije, stranke, frizerji, storitve in urniki.

---

## Zahteve

Pred zagonom mora biti na računalniku nameščeno:

- [Python 3.x](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/)

---

## Zagon projekta

**1. Kloniraj repozitorij**
```bash
git clone https://github.com/TadejSmells/OMEGA
cd OMEGA
```

**2. Zaženi Docker**

Odpri terminal v root mapi projekta (kjer sta `Dockerfile` in `docker-compose.yml`) in zaženi:
```bash
docker compose up --build
```

**3. Odpri aplikacijo v brskalniku**
```
http://localhost:8080/
```

**4. Nastavi bazo podatkov**

Ob prvem zagonu klikni na **[SISTEM] Nastavi/Osveži tabele baze** — to ustvari vse tabele v bazi.

Nato klikni **[SISTEM] Vstavi testne podatke** — to napolni bazo z vzorčnimi podatki.

---

## Struktura projekta

```
src/
├── controllers/        ← Flask za vsak user story
├── models/             ← Funkcije za branje/pisanje v bazo
│   ├── models.py       ← Definicije tabel (ne spreminjaj!!!)
│   └── model_salon.py  ← Vzorec za pisanje model funkcij
├── templates/          ← HTML strani
├── app.py              ← Glavna Flask aplikacija + vsi routi
└── db.py               ← Povezava z bazo (ne spreminjaj!!!)
```

---

## Kako dodaš svoj user story


Za vsak user story potrebuješ tri stvari:

1. `src/models/model_ime.py` — funkcije za bazo
2. `src/controllers/ime.py` — Flask logika
3. Nove route v `src/app.py` — registracija poti

Ko ustvariš controller datoteko, sporoči vodji SQLAlchemy dela, da jo doda v `app.py`.

---

## Tabele v bazi

| Tabela | Opis |
|---|---|
| `salon` | Frizerski saloni |
| `frizer` | Frizerji, vezani na salon |
| `stranka` | Stranke |
| `storitev` | Storitve in cenik |
| `urnik` | Delovni urnik frizerjev |
| `rezervacija` | Rezervacije strank |
| `uporabnik` | Uporabniki aplikacije (login) |

---

## Pogoste težave

**Docker se ne zažene**
→ Preveri, da je Docker Desktop odprt in zagnan.

**Stran ne dela / napaka ob zagonu**
→ Preveri terminal — napaka bo izpisana tam. Posreduj vodji SQLAlchemy dela.

**Stran je prazna**
→ Obišči `/polni_db` ali klikni [SISTEM] Vstavi testne podatke.

**`ModuleNotFoundError`**
→ Tvoja controller datoteka verjetno ni dodana v `app.py`. Sporoči vodji SQLAlchemy dela.

---
