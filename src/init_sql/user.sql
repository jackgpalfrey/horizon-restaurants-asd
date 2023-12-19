CREATE TABLE IF NOT EXISTS public.User
(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    username text NOT NULL UNIQUE,
    password text NOT NULL,
    full_name text NOT NULL,
    role_id integer NOT NULL DEFAULT 0,
    is_password_expired boolean NOT NULL DEFAULT true,
    branch_id uuid,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)