CREATE TABLE IF NOT EXISTS legal_entity(
  id text PRIMARY KEY NOT NULL,
  balance numeric,
  coin_symbol text);

CREATE TABLE IF NOT EXISTS txn(
  txn_hash text PRIMARY KEY NOT NULL,
  timestamp text NOT NULL,
  from_wallet text NOT NULL,
  to_wallet text NOT NULL,
  amount numeric NOT NULL,
  status text,
  FOREIGN KEY(from_wallet) REFERENCES wallet (id),
  FOREIGN KEY(to_wallet) REFERENCES wallet (id));

CREATE TABLE IF NOT EXISTS product(
  sku text PRIMARY KEY NOT NULL,
  manufacturer_id text NOT NULL,
  created_at_utc text NOT NULL,
  updated_at_utc text NOT NULL,
  flags numeric NOT NULL,
  FOREIGN KEY(manufacturer_id) REFERENCES entity (id),


CREATE TABLE IF NOT EXISTS block(
   id text PRIMARY KEY NOT NULL,
   timestamp text NOT NULL,
   transaction_id text NOT NULL,
   proof text NOT NULL,
   previous_hash numeric NOT NULL,
   FOREIGN KEY(transaction_id) REFERENCES txn (id),
