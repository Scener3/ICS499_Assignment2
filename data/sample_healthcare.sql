-- Healthcare Database with Patient PII
-- Contains: diverse international names, emails, phones, addresses

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(200)
);

INSERT INTO patients (patient_id, name, email, phone, address) VALUES
(101, 'Chen Wei', 'chen.wei@gmail.com', '(612) 555-1234', '1234 Medical Plaza, Minneapolis, MN 55401'),
(102, 'Amara Okafor', 'amara.okafor@yahoo.com', '651-555-9012', '5678 Health Drive, St Paul, MN 55101'),
(103, 'Sven Lindqvist', 'sven.lindqvist@hotmail.com', '(763) 555-7890', '9012 Wellness Way, Bloomington, MN 55420'),
(104, 'Priya Sharma', 'priya.sharma@gmail.com', '952-555-6789', '3456 Care Court, Edina, MN 55435'),
(105, 'Mohammed Al-Farsi', 'mohammed.farsi@outlook.com', '(612) 555-4567', '7890 Therapy Trail, Richfield, MN 55423'),
(106, 'Isabella Rossi', 'isabella.rossi@gmail.com', '651-555-7890', '1357 Health Circle, Burnsville, MN 55337');

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    patient_name VARCHAR(100),
    patient_email VARCHAR(100),
    patient_phone VARCHAR(30),
    appointment_date DATETIME
);

INSERT INTO appointments (appointment_id, patient_id, patient_name, patient_email, patient_phone, appointment_date) VALUES
(501, 101, 'Chen Wei', 'chen.wei@gmail.com', '(612) 555-1234', '2024-06-15 09:00:00'),
(502, 102, 'Amara Okafor', 'amara.okafor@yahoo.com', '651-555-9012', '2024-06-15 10:30:00'),
(503, 103, 'Sven Lindqvist', 'sven.lindqvist@hotmail.com', '(763) 555-7890', '2024-06-16 14:00:00'),
(504, 101, 'Chen Wei', 'chen.wei@gmail.com', '(612) 555-1234', '2024-06-17 11:00:00'),
(505, 104, 'Priya Sharma', 'priya.sharma@gmail.com', '952-555-6789', '2024-06-18 15:30:00'),
(506, 106, 'Isabella Rossi', 'isabella.rossi@gmail.com', '651-555-7890', '2024-06-19 13:00:00');