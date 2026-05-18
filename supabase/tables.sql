-- dimensions tables:
--1:
create table public.dim_customers (
  customer_id bigint null,
  customer_name text null,
  city text null,
  currency text null
) TABLESPACE pg_default;

--2:
create table public.dim_products (
  product_name text null,
  product_id bigint null,
  category text null,
  "price_INR" bigint null,
  "price_USD" double precision null
) TABLESPACE pg_default;

--3:
create table public.dim_targets_orders (
  customer_id bigint null,
  ontime_target % bigint null,
  infull_target % bigint null,
  otif_target % bigint null
) TABLESPACE pg_default;


--fact tables:
--1:
create table public.fact_aggregate (
  order_id text null,
  customer_id bigint null,
  order_placement_date date null,
  on_time bigint null,
  in_full text null,
  otif text null
) TABLESPACE pg_default;

--2:
create table public.fact_order_line (
  order_id text null,
  order_placement_date date null,
  customer_id bigint null,
  product_id bigint null,
  order_qty bigint null,
  agreed_delivery_date text null,
  actual_delivery_date text null,
  delivery_qty bigint null,
  "In Full" text null,
  "On Time" text null,
  "On Time In Full" text null
) TABLESPACE pg_default;