BEGIN;

-- salon
CREATE TABLE IF NOT EXISTS public.salon (
    id        serial PRIMARY KEY,
    ime       character varying(100) NOT NULL,
    naslov    text,
    mesto     character varying(100),
    telefon   character varying(100)
);

-- users 
CREATE TABLE IF NOT EXISTS public.users (
    id       serial PRIMARY KEY,
    username character varying(100) UNIQUE NOT NULL,
    password character varying(200) NOT NULL,
    vloga    character varying(50) DEFAULT 'stranka'
);

ALTER TABLE public.users ADD COLUMN IF NOT EXISTS vloga character varying(50) DEFAULT 'stranka';

-- frizer
CREATE TABLE IF NOT EXISTS public.frizer (
    id_frizer serial PRIMARY KEY,
    salon_id  integer REFERENCES public.salon (id),
    ime       character varying(100),
    kontakt   character varying(100),
    user_id   integer REFERENCES public.users (id) ON DELETE SET NULL
);

ALTER TABLE public.frizer ADD COLUMN IF NOT EXISTS user_id integer REFERENCES public.users (id) ON DELETE SET NULL;

-- storitev
CREATE TABLE IF NOT EXISTS public.storitev (
    id_storitve  serial PRIMARY KEY,
    ime_storitve character varying(100),
    cena         double precision,
    trajanje     time without time zone
);

-- salon ima storitve
CREATE TABLE IF NOT EXISTS public.saloni_in_storitve (
    salon_id    integer NOT NULL REFERENCES public.salon (id),
    storitev_id integer NOT NULL REFERENCES public.storitev (id_storitve),
    PRIMARY KEY (salon_id, storitev_id)
);

-- stranka
CREATE TABLE IF NOT EXISTS public.stranka (
    id_stranke    serial PRIMARY KEY,
    id_naj_frizer integer REFERENCES public.frizer (id_frizer),
    ime           character varying(100),
    priimek       character varying(100) NOT NULL,
    mail          character varying(100),
    telefon       character varying(100),
    user_id       integer REFERENCES public.users (id) ON DELETE SET NULL
);

ALTER TABLE public.stranka ADD COLUMN IF NOT EXISTS user_id integer REFERENCES public.users (id) ON DELETE SET NULL;

-- rezervacija
CREATE TABLE IF NOT EXISTS public.rezervacija (
    id_rezervacije serial PRIMARY KEY,
    id_stranke     integer REFERENCES public.stranka (id_stranke),
    id_frizerja    integer REFERENCES public.frizer (id_frizer),
    id_salona      integer REFERENCES public.salon (id),
    id_storitve    integer REFERENCES public.storitev (id_storitve),
    datum          date,
    ura            time without time zone,
    status         character varying(20) DEFAULT 'active'
        CHECK (status IN ('active', 'cancelled'))
);

ALTER TABLE public.rezervacija ADD COLUMN IF NOT EXISTS datum date;
ALTER TABLE public.rezervacija ADD COLUMN IF NOT EXISTS ura time without time zone;
ALTER TABLE public.rezervacija ADD COLUMN IF NOT EXISTS status character varying(20) DEFAULT 'active';

-- urnik
CREATE TABLE IF NOT EXISTS public.urnik (
    id_frizerja integer REFERENCES public.frizer (id_frizer),
    dan         date,
    ura         time without time zone
);

-- blokirani termini
CREATE TABLE IF NOT EXISTS public.blokiran_termin (
    id          serial PRIMARY KEY,
    id_frizerja integer NOT NULL REFERENCES public.frizer (id_frizer) ON DELETE CASCADE,
    datum       date NOT NULL,
    ura_od      time NOT NULL,
    ura_do      time NOT NULL,
    razlog      character varying(200),
    CONSTRAINT blokiran_termin_cas_check CHECK (ura_do > ura_od)
);

-- faq
CREATE TABLE IF NOT EXISTS public.faq (
    id_faq     serial PRIMARY KEY,
    vprasanje  text NOT NULL,
    odgovor    text NOT NULL,
    vrstni_red integer DEFAULT 0,
    aktiven    boolean DEFAULT true
);

-- komentarji (POSEBEJ, KER JE LAŽJE DOBIT VEN ZA VSAKO STVAR KOKR PA DODAJAM NEKE IDJE ZA REFERENCO)
CREATE TABLE IF NOT EXISTS public.komentar_salona (
    id_komentar serial PRIMARY KEY,
    id_salona   integer REFERENCES public.salon (id),
    id_stranke  integer REFERENCES public.stranka (id_stranke),
    ocena       integer CHECK (ocena >= 1 AND ocena <= 5),
    komentar    text,
    datum       timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.komentar_frizerja (
    id_komentar serial PRIMARY KEY,
    id_frizerja integer REFERENCES public.frizer (id_frizer),
    id_stranke  integer REFERENCES public.stranka (id_stranke),
    ocena       integer CHECK (ocena >= 1 AND ocena <= 5),
    komentar    text,
    datum       timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.komentar_storitve (
    id_komentar serial PRIMARY KEY,
    id_storitve integer REFERENCES public.storitev (id_storitve),
    id_stranke  integer REFERENCES public.stranka (id_stranke),
    ocena       integer CHECK (ocena >= 1 AND ocena <= 5),
    komentar    text,
    datum       timestamp DEFAULT now()
);
END;

