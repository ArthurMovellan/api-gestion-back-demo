DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS items CASCADE;

-- CREATE TABLE IF NOT EXISTS customers(
--    id_customer SERIAL PRIMARY KEY,
--    first_name VARCHAR(256),
--    last_name VARCHAR(256)
-- );

-- CREATE TABLE IF NOT EXISTS items(
--    id_item SERIAL PRIMARY KEY,
--    name_item VARCHAR(64),
--    quantity INTEGER,
--    id_customer INTEGER,
--    CONSTRAINT fk_item_customer FOREIGN KEY (id_customer) REFERENCES customers(id_customer) ON DELETE CASCADE
-- );

DROP TABLE IF EXISTS orders CASCADE;
DROP FUNCTION IF EXISTS test;
DROP FUNCTION IF EXISTS get_items_by_customer;
DROP FUNCTION IF EXISTS get_customers;

CREATE TABLE IF NOT EXISTS orders (
    id serial NOT NULL PRIMARY KEY,
    info json NOT null
);

-- INSERT INTO customers (first_name, last_name) VALUES 
-- ('Lily','Bush'),
-- ('Josh', 'Williams'),
-- ('Mary', 'Clark');

-- INSERT INTO items (name_item, quantity, id_customer) VALUES 
-- ('Computer', 5, 1),
-- ('Screen', 3, 1),
-- ('Pen', 10, 2),
-- ('Mouse', 9, 2),
-- ('Bag', 2, 2),
-- ('Car', 1, 3)

INSERT INTO orders (info)
VALUES('{ "customer": "Lily Bush", "items": [{"product": "Diaper","qty": 24},{"product": "Bag", "qty": 31}]}'),
      ('{ "customer": "Josh William", "items": [{"product": "Toy Car","qty": 1}]}'),
      ('{ "customer": "Mary Clark", "items": [{"product": "Toy Train","qty": 2}]}');

CREATE FUNCTION get_items_by_customer (cust json)
    returns json
language sql  
as
$$
    select info -> 'items'  AS items
    from orders
    WHERE info ->> 'customer' like cust ->> 'customer'
$$;

CREATE FUNCTION get_customers ()
    returns json
language sql
as
$$
    select info -> 'customer' AS customers
    from orders
$$;
