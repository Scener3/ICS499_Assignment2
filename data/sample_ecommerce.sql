-- E-commerce Database with Customer PII
-- Contains: diverse names, emails, phones, addresses

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(200)
);

INSERT INTO customers (customer_id, name, email, phone, address) VALUES
(1, 'Rajesh Patel', 'rajesh.patel@gmail.com', '612-555-1234', '123 Main Street, Minneapolis, MN 55401'),
(2, 'Maria García', 'maria.garcia@yahoo.com', '651-555-5678', '456 Oak Avenue, St Paul, MN 55101'),
(3, 'Rajesh Patel', 'rajesh.patel@gmail.com', '612-555-1234', '123 Main Street, Minneapolis, MN 55401'),
(4, 'Yuki Tanaka', 'yuki.tanaka@outlook.com', '763-555-9012', '789 Pine Road, Bloomington, MN 55420'),
(5, 'Fatima Al-Rashid', 'fatima.rashid@hotmail.com', '952-555-3456', '321 Lake Drive, Edina, MN 55435'),
(6, 'Kwame Osei', 'kwame.osei@gmail.com', '612-555-7890', '654 River Lane, Richfield, MN 55423'),
(7, 'Ingrid Svensson', 'ingrid.svensson@yahoo.com', '651-555-2345', '987 Forest Blvd, Eagan, MN 55122');

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    shipping_address VARCHAR(200),
    contact_phone VARCHAR(30)
);

INSERT INTO orders (order_id, customer_id, customer_name, customer_email, shipping_address, contact_phone) VALUES
(1001, 1, 'Rajesh Patel', 'rajesh.patel@gmail.com', '123 Main Street, Minneapolis, MN 55401', '612-555-1234'),
(1002, 2, 'Maria García', 'maria.garcia@yahoo.com', '456 Oak Avenue, St Paul, MN 55101', '651-555-5678'),
(1003, 1, 'Rajesh Patel', 'rajesh.patel@gmail.com', '123 Main Street, Minneapolis, MN 55401', '612-555-1234'),
(1004, 4, 'Yuki Tanaka', 'yuki.tanaka@outlook.com', '789 Pine Road, Bloomington, MN 55420', '763-555-9012'),
(1005, 6, 'Kwame Osei', 'kwame.osei@gmail.com', '654 River Lane, Richfield, MN 55423', '612-555-7890');