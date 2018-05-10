DELETE FROM legal_entity;
DELETE FROM txn;
DELETE FROM product;

CREATE TABLE IF NOT EXISTS legal_entity(
  id text PRIMARY KEY NOT NULL,
  name text,
  desc text,
  email text,
  address text,
  flags numeric,
  created_at_utc text,
  updated_at_utc text);

CREATE TABLE IF NOT EXISTS txn(
  id text PRIMARY KEY NOT NULL,
  created_at_utc text NOT NULL,
  from_legal_entity text NOT NULL,
  to_legal_entity text NOT NULL,
  product_sku text NOT NULL,
  quantity numeric NOT NULL);


CREATE TABLE IF NOT EXISTS product(
  sku text PRIMARY KEY NOT NULL,
  flags numeric,
  description text,
  weight text,
  size_x numeric,
  size_y numeric,
  size_z numeric,
  manufacturer_id text NOT NULL,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL);


-- CREATE TABLE IF NOT EXISTS block(
--    id text PRIMARY KEY NOT NULL,
--    timestamp text NOT NULL,
--    transaction_id text NOT NULL,
--    proof text NOT NULL,
--    previous_hash numeric NOT NULL,
--    FOREIGN KEY(transaction_id) REFERENCES txn (id),
