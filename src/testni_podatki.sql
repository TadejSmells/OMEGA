TRUNCATE salon,
frizer,
stranka,
storitev,
rezervacija,
urnik,
saloni_in_storitve RESTART IDENTITY CASCADE;

INSERT INTO
    salon (ime, naslov, mesto, telefon)
VALUES (
        'Salon Lepote',
        'Glavna ulica 1',
        'Ljubljana',
        '01-123-456'
    ),
    (
        'Frizerski Studio',
        'Cesta 2',
        'Maribor',
        '02-654-321'
    ),
    (
        'Salon Elegance',
        'Ulica 3',
        'Celje',
        '03-789-012'
    )
ON CONFLICT DO NOTHING;

INSERT INTO
    frizer (salon_id, ime, kontakt)
VALUES (1, 'Ana Kovač', '031-555-666'),
    (
        2,
        'Tina Zupan',
        '041-777-888'
    ),
    (
        3,
        'Miha Novak',
        '040-999-000'
    )
ON CONFLICT DO NOTHING;

INSERT INTO
    stranka (ime, priimek, mail, telefon)
VALUES (
        'Luka',
        'Novak',
        'luka@test.si',
        '031-999-888'
    ),
    (
        'Damjan',
        'Kovac',
        'damjan@test.si',
        '031-777-858'
    ),
    (
        'Zoja',
        'Luč',
        'zoja@test.si',
        '041-342-678'
    ),
    (
        'Maja',
        'Kralj',
        'maja@test.si',
        '031-111-222'
    )
ON CONFLICT DO NOTHING;

INSERT INTO
    storitev (ime_storitve, cena, trajanje)
VALUES (
        'Upravljanje s kosmetskimi izdelki',
        50.0,
        '01:00:00'
    ),
    (
        'Barvanje las',
        70.0,
        '01:30:00'
    )
ON CONFLICT DO NOTHING;

INSERT INTO
    saloni_in_storitve (salon_id, storitev_id)
VALUES (1, 1),
    (1, 2),
    (2, 2),
    (3, 1),
    (3, 2)
ON CONFLICT DO NOTHING;

INSERT INTO
    faq (
        vprasanje,
        odgovor,
        vrstni_red,
        aktiven
    )
VALUES (
        'Kako rezerviram termin?',
        'Termin rezerviraš prek naše spletne strani v razdelku Rezervacije. Izberi frizerjа, datum in uro.',
        1,
        TRUE
    ),
    (
        'Ali lahko odpovem rezervacijo?',
        'Da, rezervacijo lahko odpoveš najkasneje 24 ur pred terminom.',
        2,
        TRUE
    ),
    (
        'Kakšne so možnosti plačila?',
        'Sprejemamo gotovino in kartično plačilo na mestu.',
        3,
        TRUE
    ),
    (
        'Kako dolgo traja barvanje las?',
        'Barvanje las traja približno 1,5 ure, odvisno od dolžine in tehnike.',
        4,
        TRUE
    ),
    (
        'Ali potrebujem predhodni termin?',
        'Priporočamo predhodno rezervacijo, a sprejemamo tudi stranke brez termina, če je prosto mesto.',
        5,
        TRUE
    )
ON CONFLICT DO NOTHING;