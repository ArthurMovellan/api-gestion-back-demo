DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS items CASCADE;

CREATE TABLE IF NOT EXISTS customers(
   id_customer SERIAL PRIMARY KEY,
   first_name VARCHAR(256),
   last_name VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS items(
   id_item SERIAL PRIMARY KEY,
   name_item VARCHAR(64),
   quantity INTEGER,
   id_customer INTEGER,
   CONSTRAINT fk_item_customer FOREIGN KEY (id_customer) REFERENCES customers(id_customer) ON DELETE CASCADE
);

INSERT INTO customers (first_name, last_name) VALUES 
('Lily','Bush'),
('Josh', 'Williams'),
('Mary', 'Clark');

INSERT INTO items (name_item, quantity, id_customer) VALUES 
('Computer', 5, 1),
('Screen', 3, 1),
('Pen', 10, 2),
('Mouse', 9, 2),
('Bag', 2, 2),
('Car', 1, 3)