
-- Testne rezervacije z datumi
INSERT INTO rezervacija (id_stranke, id_frizerja, id_salona, id_storitve, datum, ura)
VALUES
    (1, 1, 1, 1, '2026-05-05', '09:00:00'),
    (2, 2, 2, 2, '2026-05-06', '10:30:00'),
    (3, 3, 3, 1, '2026-05-07', '14:00:00'),
    (4, 1, 1, 2, '2026-05-08', '11:00:00')
ON CONFLICT DO NOTHING;
