-- Human Resources Database with Employee PII
-- Contains: diverse global names, emails, phones, addresses

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(200)
);

INSERT INTO employees (employee_id, name, email, phone, address) VALUES
(201, 'Anastasia Petrova', 'anastasia.petrova@gmail.com', '612-555-1001', '100 Corporate Drive, Minneapolis, MN 55401'),
(202, 'Hiroshi Yamamoto', 'hiroshi.yamamoto@yahoo.com', '612-555-1002', '200 Business Blvd, St Paul, MN 55101'),
(203, 'Zainab Hassan', 'zainab.hassan@hotmail.com', '612-555-1003', '300 Enterprise Ave, Bloomington, MN 55420'),
(204, 'Carlos Rodriguez', 'carlos.rodriguez@outlook.com', '612-555-1004', '400 Innovation Way, Edina, MN 55435'),
(205, 'Nina Kowalski', 'nina.kowalski@gmail.com', '612-555-1005', '500 Technology Park, Richfield, MN 55423'),
(206, 'Ahmed El-Sayed', 'ahmed.sayed@yahoo.com', '612-555-1006', '600 Tech Center, Maple Grove, MN 55369'),
(207, 'Sofia Andersson', 'sofia.andersson@hotmail.com', '612-555-1007', '700 Innovation Blvd, Plymouth, MN 55441');

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    manager_name VARCHAR(100),
    manager_email VARCHAR(100),
    manager_phone VARCHAR(30)
);

INSERT INTO departments (department_id, department_name, manager_name, manager_email, manager_phone) VALUES
(301, 'Engineering', 'Anastasia Petrova', 'anastasia.petrova@gmail.com', '612-555-1001'),
(302, 'Sales', 'Hiroshi Yamamoto', 'hiroshi.yamamoto@yahoo.com', '612-555-1002'),
(303, 'Marketing', 'Zainab Hassan', 'zainab.hassan@hotmail.com', '612-555-1003'),
(304, 'HR', 'Carlos Rodriguez', 'carlos.rodriguez@outlook.com', '612-555-1004'),
(305, 'Finance', 'Nina Kowalski', 'nina.kowalski@gmail.com', '612-555-1005');