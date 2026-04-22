# OMEGA

!!! PRED DELANJEM USER STORYJA SPOROČITE VODJI TISTEGA DELA !!!
Za vse modele in controllerje kontaktirajte vodji podatkovne baze in SQLAlchemy!

Repozitorij za skupino Omega

Projekt Omega (Managment frizerskih salonov)

Kako zagnati ta projekt:

1. Nujno rabi bit na računalniku PREJ nameščeno:

   - Python
   - Docker Desktop
   - VsCode
2. kloniraj reposetorij na računalnik
   git clone https://github.com/TadejSmells/OMEGA
3. v root mapi projekta (torej tam kjer vidis DockerFile, dockercompose...) odpreš terminal in zaženeš ukaz:
   docker compose up --build
4. v brskalniku odpreš http://localhost:8080/
5. klikneš na  [SISTEM] Nastavi/Osveži tabele baze, da postaviš bazo


KAKO DELAT FUNKCIJE:

1. Naredimo 3 datoteke,
   1. "ime_datoteke.py v mapi src/controllers
   2. "ime_datoteke.py v mapi src/models
   3. "ime_datoteke.html v mapi src/templates
   4. dodat import controller datoteke v app.py
   5. dodat pot v app.py

"Vse model datoteke morajo uporabljati db.get_session() in try/finally. Primer je v models/model_frizer.py."

