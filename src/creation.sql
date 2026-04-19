BEGIN;


CREATE TABLE IF NOT EXISTS public.frizer
(
    id_frizer serial NOT NULL,
    salon_id integer,
    ime character varying(100) COLLATE pg_catalog."default",
    kontakt character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT frizer_pkey PRIMARY KEY (id_frizer)
);

CREATE TABLE IF NOT EXISTS public.rezervacija
(
    id_rezervacije serial NOT NULL,
    id_stranke integer,
    id_frizerja integer,
    id_salona integer,
    id_storitve integer,
    CONSTRAINT rezervacija_pkey PRIMARY KEY (id_rezervacije)
);

CREATE TABLE IF NOT EXISTS public.salon
(
    id serial NOT NULL,
    ime character varying(100) COLLATE pg_catalog."default" NOT NULL,
    naslov text COLLATE pg_catalog."default",
    mesto character varying(100) COLLATE pg_catalog."default",
    telefon character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT salon_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.storitev
(
    id_storitve serial NOT NULL,
    ime_storitve character varying(100) COLLATE pg_catalog."default",
    cena double precision,
    trajanje time without time zone,
    CONSTRAINT storitev_pkey PRIMARY KEY (id_storitve),
);

CREATE TABLE IF NOT EXISTS public.salon_storitev
(
    salon_id    integer NOT NULL,
    storitev_id integer NOT NULL,
    CONSTRAINT salon_storitev_pkey PRIMARY KEY (salon_id, storitev_id)
);

CREATE TABLE IF NOT EXISTS public.stranka
(
    id_stranke serial NOT NULL,
    id_naj_frizer integer,
    ime character varying(100) COLLATE pg_catalog."default",
    mail character varying(100) COLLATE pg_catalog."default",
    telefon character varying(100) COLLATE pg_catalog."default",
    priimek character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT stranka_pkey PRIMARY KEY (id_stranke)
);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.urnik
(
    id_frizerja integer,
    dan date,
    ura time without time zone
);

CREATE TABLE IF NOT EXISTS faq (
    id_faq       SERIAL PRIMARY KEY,
    vprasanje    TEXT NOT NULL,   -- question
    odgovor      TEXT NOT NULL,   -- answer
    vrstni_red   INT DEFAULT 0,   -- sort order
    aktiven      BOOLEAN DEFAULT TRUE
);
ALTER TABLE IF EXISTS public.frizer
    ADD CONSTRAINT frizer_salon_id_fkey FOREIGN KEY (salon_id)
    REFERENCES public.salon (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.rezervacija
    ADD CONSTRAINT rezervacija_id_frizerja_fkey FOREIGN KEY (id_frizerja)
    REFERENCES public.frizer (id_frizer) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.rezervacija
    ADD CONSTRAINT rezervacija_id_salona_fkey FOREIGN KEY (id_salona)
    REFERENCES public.salon (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.rezervacija
    ADD CONSTRAINT rezervacija_id_storitve_fkey FOREIGN KEY (id_storitve)
    REFERENCES public.storitev (id_storitve) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.rezervacija
    ADD CONSTRAINT rezervacija_id_stranke_fkey FOREIGN KEY (id_stranke)
    REFERENCES public.stranka (id_stranke) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.urnik
    ADD CONSTRAINT urnik_id_frizerja_fkey FOREIGN KEY (id_frizerja)
    REFERENCES public.frizer (id_frizer) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;
