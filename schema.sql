-- basic structure for testing
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT,
    price INT,
    color VARCHAR(30)
);

INSERT INTO cars (make, model, year, price, color) VALUES
('Toyota', 'Camry', 2021, 25000, 'Blue'),
('Honda', 'Accord', 2022, 28000, 'Red'),
('Ford', 'Mustang', 2023, 45000, 'Black'),
('Toyota', 'RAV4', 2022, 32000, 'Red'),
('Tesla', 'Model 3', 2023, 50000, 'White');