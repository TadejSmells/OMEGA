TRUNCATE salon,
frizer,
stranka,
storitev,
rezervacija,
urnik,
saloni_in_storitve,
blokiran_termin,
users,
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

INSERT INTO
    rezervacija (
        id_stranke,
        id_frizerja,
        id_salona,
        id_storitve,
        datum,
        ura,
        status
    )
VALUES (
        1,
        1,
        1,
        1,
        '2024-07-01',
        '10:00:00',
        'active'
    ),
    (
        2,
        2,
        2,
        2,
        '2024-07-02',
        '11:30:00',
        'active'
    ),
    (
        3,
        3,
        3,
        1,
        '2024-07-03',
        '14:00:00',
        'cancelled'
    ),
    (
        4,
        1,
        1,
        2,
        '2024-07-04',
        '09:30:00',
        'cancelled'
    )
ON CONFLICT DO NOTHING;
INSERT INTO urnik (id_frizerja, dan, ura) VALUES
    -- Ana: pon–pet 9:00–16:00
    (1, '2024-07-01', '09:00:00'), (1, '2024-07-01', '10:00:00'),
    (1, '2024-07-01', '11:00:00'), (1, '2024-07-01', '12:00:00'),
    (1, '2024-07-01', '13:00:00'), (1, '2024-07-01', '14:00:00'),
    (1, '2024-07-01', '15:00:00'), (1, '2024-07-01', '16:00:00'),
    (1, '2024-07-02', '09:00:00'), (1, '2024-07-02', '10:00:00'),
    (1, '2024-07-02', '11:00:00'), (1, '2024-07-02', '12:00:00'),
    -- Tina: pon–sre 10:00–17:00
    (2, '2024-07-01', '10:00:00'), (2, '2024-07-01', '11:00:00'),
    (2, '2024-07-01', '12:00:00'), (2, '2024-07-01', '13:00:00'),
    (2, '2024-07-01', '14:00:00'), (2, '2024-07-01', '15:00:00'),
    (2, '2024-07-02', '10:00:00'), (2, '2024-07-02', '11:00:00'),
    (2, '2024-07-02', '12:00:00'), (2, '2024-07-02', '13:00:00'),
    -- Miha: tor–pet 08:00–15:00
    (3, '2024-07-02', '08:00:00'), (3, '2024-07-02', '09:00:00'),
    (3, '2024-07-02', '10:00:00'), (3, '2024-07-02', '11:00:00'),
    (3, '2024-07-02', '12:00:00'), (3, '2024-07-02', '13:00:00'),
    (3, '2024-07-03', '08:00:00'), (3, '2024-07-03', '09:00:00'),
    (3, '2024-07-03', '10:00:00'), (3, '2024-07-03', '11:00:00');

INSERT INTO blokiran_termin (id_frizerja, datum, ura_od, ura_do, razlog) VALUES
    (1, '2024-07-03', '12:00:00', '14:00:00', 'Kosilo'),
    (2, '2024-07-04', '09:00:00', '17:00:00', 'Dopust'),
    (3, '2024-07-05', '08:00:00', '10:00:00', 'Sestanek');
ON CONFLICT DO NOTHING;