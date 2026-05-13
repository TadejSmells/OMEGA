TRUNCATE salon,
frizer,
stranka,
storitev,
rezervacija,
urnik,
saloni_in_storitve,
blokiran_termin,
users,
faq RESTART IDENTITY CASCADE;

-- ── HARDCODED ADMIN (username: admin123 / password: admin123) ─────────────────
INSERT INTO users (username, password, vloga)
VALUES (
    'admin123',
    'scrypt:32768:8:1$Z53od1RwDEMM8PBF$5448c3c5f31ee76814f4948936fd4351499735ca1435a2feaf3a8aee35e0390262548ecbf47b1d8ddf1e4e4230bd1fab3026e744b714a6c130e491696df46558',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- ── SALONI ────────────────────────────────────────────────────────────────────
INSERT INTO salon (ime, naslov, mesto, telefon)
VALUES
    ('Salon Lepote',     'Glavna ulica 1', 'Ljubljana', '01-123-456'),
    ('Frizerski Studio', 'Cesta 2',        'Maribor',   '02-654-321'),
    ('Salon Elegance',   'Ulica 3',        'Celje',     '03-789-012')
ON CONFLICT DO NOTHING;

-- ── FRIZERJI ──────────────────────────────────────────────────────────────────
INSERT INTO frizer (salon_id, ime, kontakt)
VALUES
    (1, 'Ana Kovač',  '031-555-666'),
    (2, 'Tina Zupan', '041-777-888'),
    (3, 'Miha Novak', '040-999-000')
ON CONFLICT DO NOTHING;

-- ── STRANKE ───────────────────────────────────────────────────────────────────
INSERT INTO stranka (ime, priimek, mail, telefon)
VALUES
    ('Luka',    'Novak',     'luka@test.si',      '031-999-888'),
    ('Damjan',  'Kovac',     'damjan@test.si',    '031-777-858'),
    ('Zoja',    'Luč',       'zoja@test.si',      '041-342-678'),
    ('Maja',    'Kralj',     'maja@test.si',      '031-111-222'),
    ('Ana',     'Horvat',    'ana@test.si',       '040-123-456'),
    ('Miha',    'Zupan',     'miha@test.si',      '031-234-567'),
    ('Sara',    'Mlakar',    'sara@test.si',      '041-345-678'),
    ('Tilen',   'Kranjc',    'tilen@test.si',     '051-456-789'),
    ('Nika',    'Vidmar',    'nika@test.si',      '040-567-890'),
    ('Jan',     'Kos',       'jan@test.si',       '031-678-901'),
    ('Eva',     'Turk',      'eva@test.si',       '041-789-012'),
    ('Marko',   'Potočnik',  'marko@test.si',     '051-890-123'),
    ('Tjaša',   'Bizjak',    'tjasa@test.si',     '040-901-234'),
    ('Nejc',    'Petek',     'nejc@test.si',      '031-112-233'),
    ('Klara',   'Golob',     'klara@test.si',     '041-223-344'),
    ('Rok',     'Božič',     'rok@test.si',       '051-334-455'),
    ('Urška',   'Korošec',   'urska@test.si',     '040-445-566'),
    ('Jure',    'Hribar',    'jure@test.si',      '031-556-677'),
    ('Pia',     'Bavdek',    'pia@test.si',       '041-667-788'),
    ('Aljaž',   'Rozman',    'aljaz@test.si',     '051-778-899')
ON CONFLICT DO NOTHING;

-- ── STORITVE ──────────────────────────────────────────────────────────────────
INSERT INTO storitev (ime_storitve, cena, trajanje)
VALUES
    ('Upravljanje s kosmetskimi izdelki', 50.0, '01:00:00'),
    ('Barvanje las',                       70.0, '01:30:00')
ON CONFLICT DO NOTHING;

INSERT INTO saloni_in_storitve (salon_id, storitev_id)
VALUES (1, 1), (1, 2), (2, 2), (3, 1), (3, 2)
ON CONFLICT DO NOTHING;

-- ── FAQ ───────────────────────────────────────────────────────────────────────
INSERT INTO faq (vprasanje, odgovor, vrstni_red, aktiven)
VALUES
    ('Kako rezerviram termin?',
     'Termin rezerviraš prek naše spletne strani v razdelku Rezervacije. Izberi frizerja, datum in uro.',
     1, TRUE),
    ('Ali lahko odpovem rezervacijo?',
     'Da, rezervacijo lahko odpoveš najkasneje 24 ur pred terminom.',
     2, TRUE),
    ('Kakšne so možnosti plačila?',
     'Sprejemamo gotovino in kartično plačilo na mestu.',
     3, TRUE),
    ('Kako dolgo traja barvanje las?',
     'Barvanje las traja približno 1,5 ure, odvisno od dolžine in tehnike.',
     4, TRUE),
    ('Ali potrebujem predhodni termin?',
     'Priporočamo predhodno rezervacijo, a sprejemamo tudi stranke brez termina, če je prosto mesto.',
     5, TRUE)
ON CONFLICT DO NOTHING;

-- ── REZERVACIJE ───────────────────────────────────────────────────────────────
INSERT INTO rezervacija (id_stranke, id_frizerja, id_salona, id_storitve, datum, ura, status)
VALUES
    (1, 1, 1, 1, '2026-05-07', '10:00:00', 'active'),
    (2, 2, 2, 2, '2026-05-07', '11:30:00', 'active'),
    (3, 3, 3, 1, '2026-05-07', '14:00:00', 'cancelled'),
    (4, 1, 1, 2, '2026-05-07', '09:30:00', 'cancelled')
ON CONFLICT DO NOTHING;

-- ── URNIK ─────────────────────────────────────────────────────────────────────
INSERT INTO urnik (id_frizerja, dan, ura) VALUES
    -- Ana: pon–pet 9:00–16:00
    (1, '2026-05-07', '09:00:00'), (1, '2026-05-07', '10:00:00'),
    (1, '2026-05-07', '11:00:00'), (1, '2026-05-07', '12:00:00'),
    (1, '2026-05-07', '13:00:00'), (1, '2026-05-07', '14:00:00'),
    (1, '2026-05-07', '15:00:00'), (1, '2026-05-07', '16:00:00'),
    (1, '2026-05-08', '09:00:00'), (1, '2026-05-08', '10:00:00'),
    (1, '2026-05-08', '11:00:00'), (1, '2026-05-08', '12:00:00'),
    -- Tina: pon–sre 10:00–17:00
    (2, '2026-05-07', '10:00:00'), (2, '2026-05-07', '11:00:00'),
    (2, '2026-05-07', '12:00:00'), (2, '2026-05-07', '13:00:00'),
    (2, '2026-05-07', '14:00:00'), (2, '2026-05-07', '15:00:00'),
    (2, '2026-05-08', '10:00:00'), (2, '2026-05-08', '11:00:00'),
    (2, '2026-05-08', '12:00:00'), (2, '2026-05-08', '13:00:00'),
    -- Miha: tor–pet 08:00–15:00
    (3, '2026-05-08', '08:00:00'), (3, '2026-05-08', '09:00:00'),
    (3, '2026-05-08', '10:00:00'), (3, '2026-05-08', '11:00:00'),
    (3, '2026-05-08', '12:00:00'), (3, '2026-05-08', '13:00:00'),
    (3, '2026-05-09', '08:00:00'), (3, '2026-05-09', '09:00:00'),
    (3, '2026-05-09', '10:00:00'), (3, '2026-05-09', '11:00:00');

-- ── BLOKIRANI TERMINI ─────────────────────────────────────────────────────────
INSERT INTO blokiran_termin (id_frizerja, datum, ura_od, ura_do, razlog) VALUES
    (1, '2026-05-07', '12:00:00', '14:00:00', 'Kosilo'),
    (2, '2026-05-08', '09:00:00', '17:00:00', 'Dopust'),
    (3, '2026-05-09', '08:00:00', '10:00:00', 'Sestanek');

--13/05/26: testni podatki za priljubljene vse, komentarji, še testni uporabniki(na njih so fav/komentarji)
-- up:stranka123    geslo: stranka123
-- up:frizer123     geslo: frizer123
INSERT INTO users (username, password, vloga) VALUES
    ('stranka123',
     'scrypt:32768:8:1$xtNfx7F7ooSrRTMI$66e165041671151e58141e9b52934609c4ecbe46da0172f335a42f1282151ed2f063a9c7392ada53fe8d29d2c5c6a23d934f93df1900170a6e9f2bfa9ab8a812',
     'stranka'),
    ('frizer123',
     'scrypt:32768:8:1$FG79VGxms9nbcxZ8$3a52dfa96e23111af0ea94163f6dd082e470c82cae4f652957a4b1e8a043931d255621fabe5e971a89a01bc818ff6036fcb46d002b10da4f01d144d686dbc765',
     'frizer')
ON CONFLICT (username) DO NOTHING;

--insert v tabelo stranka  
INSERT INTO stranka (ime, priimek, mail, telefon, user_id, id_naj_frizer)
SELECT 'Testna', 'Stranka', 'stranka@test.si', '040-000-001',
       u.id,
       (SELECT id_frizer FROM frizer WHERE ime = 'Ana Kovač')   -- najljubši frizer
FROM users u
WHERE u.username = 'stranka123'
ON CONFLICT DO NOTHING;

-- insertv v tabelo frizer
INSERT INTO frizer (salon_id, ime, kontakt, user_id)
SELECT 1, 'Testni Frizer', '040-000-002', u.id
FROM users u
WHERE u.username = 'frizer123'
ON CONFLICT DO NOTHING;

-- Najljubši saloni
INSERT INTO priljubljeni_saloni (id_stranke, id_salona) VALUES
    ((SELECT id_stranke FROM stranka WHERE ime = 'Testna'), 1),
    ((SELECT id_stranke FROM stranka WHERE ime = 'Testna'), 2)
ON CONFLICT DO NOTHING;

-- Najljubši frizerji
INSERT INTO priljubljeni_frizerji (id_stranke, id_frizerja) VALUES
    ((SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'), 1),  
    ((SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'), 3)
ON CONFLICT DO NOTHING;

-- Najljubše storitve
INSERT INTO priljubljene_storitve (id_stranke, id_storitve) VALUES
    ((SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'), 1), 
    ((SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'), 2)  
ON CONFLICT DO NOTHING;

-- ── Komentarji salonov ──
INSERT INTO komentar_salona (id_salona, id_stranke, ocena, komentar, datum) VALUES
    (1, 1, 5, 'Vrhunska storitev, prijazno osebje. Definitivno se vrnem!',           '2026-05-01 14:20'),
    (1, 5, 4, 'Lepo urejen salon, le na termin sem čakala kar nekaj časa.',          '2026-04-22 10:05'),
    (1, (SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'),
        5, 'Ana je čudovita frizerka, salon pa zelo prijeten. Priporočam!',          '2026-05-10 16:45'),
    (2, 2, 4, 'Profesionalen pristop, cene pa malce višje od povprečja.',            '2026-04-30 11:00'),
    (2, 9, 3, 'V redu izkušnja, ničesar posebnega.',                                 '2026-04-15 09:30'),
    (3, 3, 5, 'Najboljši salon v Celju! Miha je pravi mojster.',                     '2026-05-05 17:10'),
    (3, 7, 4, 'Zelo dobro, samo parkirišča je premalo.',                             '2026-04-28 13:15')
ON CONFLICT DO NOTHING;

-- ── Komentarji frizerjev ──
INSERT INTO komentar_frizerja (id_frizerja, id_stranke, ocena, komentar, datum) VALUES
    (1, 1, 5, 'Ana je natančna in zelo prijazna. Vedno odlična frizura.',            '2026-05-01 14:25'),
    (1, 5, 5, 'Najboljša frizerka v Ljubljani, brez dvoma.',                         '2026-04-22 10:10'),
    (1, (SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'),
        5, 'Razume, kaj rabim, brez dolgih razlag. Top!',                            '2026-05-10 16:50'),
    (2, 2, 4, 'Tina dobro svetuje pri barvanju las.',                                '2026-04-30 11:05'),
    (3, 3, 5, 'Miha je čaroben — kratke pričeske so njegov forte.',                  '2026-05-05 17:15'),
    (3, 7, 4, 'Hiter in učinkovit, brez nepotrebnega klepetanja.',                   '2026-04-28 13:20')
ON CONFLICT DO NOTHING;

-- ── Komentarji storitev ──
INSERT INTO komentar_storitve (id_storitve, id_stranke, ocena, komentar, datum) VALUES
    (1, 1, 5, 'Odlična kakovost izdelkov, učinek viden takoj.',                      '2026-05-01 14:30'),
    (1, 3, 4, 'V redu, le cena bi lahko bila nižja.',                                '2026-05-05 17:20'),
    (2, 2, 5, 'Barva je popolnoma takšna, kot sem želela.',                          '2026-04-30 11:10'),
    (2, 5, 4, 'Trajalo malo dlje od napovedanega, sicer pa OK.',                     '2026-04-22 10:15'),
    (2, (SELECT id_stranke FROM stranka WHERE mail = 'stranka@test.si'),
        5, 'Barvanje las brez poškodb — natančen postopek.',                         '2026-05-10 17:00')
ON CONFLICT DO NOTHING;