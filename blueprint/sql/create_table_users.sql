CREATE TABLE IF NOT EXISTS public.users
(
    u_id serial NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    surname text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    login text COLLATE pg_catalog."default" NOT NULL,
    hash_password text COLLATE pg_catalog."default" NOT NULL,
    role_id integer,
    CONSTRAINT users_pkey PRIMARY KEY (u_id),
    CONSTRAINT users_fkey FOREIGN KEY (role_id)
        REFERENCES public.roles (r_id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;