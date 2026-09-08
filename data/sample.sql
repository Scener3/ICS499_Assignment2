-- Sample database with PII for testing
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200)
);

INSERT INTO customers (customer_id, name, email, phone, address) VALUES
(1, 'John Smith', 'john.smith@gmail.com', '612-555-1234', '123 Main Street, Minneapolis, MN 55401'),
(2, 'Jane Doe', 'jane.doe@yahoo.com', '651-555-5678', '456 Oak Avenue, St Paul, MN 55101'),
(3, 'John Smith', 'john.smith@gmail.com', '612-555-1234', '123 Main Street, Minneapolis, MN 55401'),
(4, 'Bob Johnson', 'bob.johnson@hotmail.com', '763-555-9012', '789 Pine Road, Bloomington, MN 55420');

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    shipping_address VARCHAR(200),
    contact_phone VARCHAR(20)
);

INSERT INTO orders (order_id, customer_id, customer_name, customer_email, shipping_address, contact_phone) VALUES
(1001, 1, 'John Smith', 'john.smith@gmail.com', '123 Main Street, Minneapolis, MN 55401', '612-555-1234'),
(1002, 2, 'Jane Doe', 'jane.doe@yahoo.com', '456 Oak Avenue, St Paul, MN 55101', '651-555-5678'),
(1003, 1, 'John Smith', 'john.smith@gmail.com', '123 Main Street, Minneapolis, MN 55401', '612-555-1234');