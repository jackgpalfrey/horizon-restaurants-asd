CREATE TABLE IF NOT EXISTS public.order (
id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
status int NOT NULL DEFAULT 1,
number int NOT NULL,
priority int NOT NULL DEFAULT 0,
customer_name text,
branch_id uuid NOT NULL,
table_id uuid,
assigned_staff uuid,
custom_discount_multiplier decimal(3,2) NOT NULL DEFAULT 1.0,
discount_id uuid,
final_price decimal(3,2),
PRIMARY KEY (id),
CONSTRAINT fk_branch FOREIGN KEY (branch_id) 
    REFERENCES branch(id) ON DELETE CASCADE,
CONSTRAINT fk_staff FOREIGN KEY (assigned_staff)
    REFERENCES staff(id) ON DELETE SET NULL,
CONSTRAINT fk_table FOREIGN KEY (table_id)
    REFERENCES public.table(id) ON DELETE SET NULL,
CONSTRAINT fk_discount FOREIGN KEY (discount_id)
    REFERENCES public.discounts ON DELETE SET NULL
)
