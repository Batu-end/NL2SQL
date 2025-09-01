-- basic structure for testing
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT,
    price INT,
    color VARCHAR(30)
);
