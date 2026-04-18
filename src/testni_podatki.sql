TRUNCATE salon,
frizer,
stranka,
storitev,
rezervacija,
urnik RESTART IDENTITY CASCADE;

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