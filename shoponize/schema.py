"""SQLite schema and seed data for local development and tests."""

from __future__ import annotations

from typing import Any


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customer (
    customerID INTEGER PRIMARY KEY,
    age INTEGER CHECK (age IS NULL OR age >= 0),
    date_of_birth TEXT,
    name_first TEXT,
    name_middle TEXT,
    name_last TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('M', 'F', 'O')),
    loginAttempts INTEGER NOT NULL DEFAULT 0,
    isLocked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contactNumber_customer (
    customerID INTEGER NOT NULL,
    number TEXT NOT NULL,
    PRIMARY KEY (customerID, number),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customerProfile (
    customerID INTEGER PRIMARY KEY,
    address_street_name TEXT,
    address_street_number TEXT,
    address_city TEXT,
    address_state TEXT,
    address_zipcode TEXT,
    payment TEXT,
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS productCategory (
    categoryID INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS product (
    productID INTEGER PRIMARY KEY,
    description TEXT,
    quantityAvailable INTEGER NOT NULL DEFAULT 0 CHECK (quantityAvailable >= 0),
    price REAL NOT NULL CHECK (price >= 0),
    name TEXT NOT NULL,
    review TEXT,
    categoryID INTEGER,
    isLowStock INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS orders (
    orderNumber INTEGER PRIMARY KEY,
    customerID INTEGER NOT NULL,
    orderDate TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    orderStatus TEXT NOT NULL CHECK (orderStatus IN ('Pending', 'In Progress', 'Delivered', 'Cancelled')),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS contains (
    orderNumber INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unitPrice REAL NOT NULL DEFAULT 0 CHECK (unitPrice >= 0),
    PRIMARY KEY (orderNumber, productID),
    FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS admin (
    adminID INTEGER PRIMARY KEY,
    name_first TEXT,
    name_middle TEXT,
    name_last TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    address_street_name TEXT,
    address_street_number TEXT,
    address_city TEXT,
    address_state TEXT,
    address_zipcode TEXT,
    loginAttempts INTEGER NOT NULL DEFAULT 0,
    isLocked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contactNumber_admin (
    adminID INTEGER NOT NULL,
    number TEXT NOT NULL,
    PRIMARY KEY (adminID, number),
    FOREIGN KEY (adminID) REFERENCES admin(adminID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS manages (
    adminID INTEGER NOT NULL,
    categoryID INTEGER NOT NULL,
    PRIMARY KEY (adminID, categoryID),
    FOREIGN KEY (adminID) REFERENCES admin(adminID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS supplier (
    supplierID INTEGER PRIMARY KEY,
    name_first TEXT,
    name_middle TEXT,
    name_last TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    address_street_name TEXT,
    address_street_number TEXT,
    address_city TEXT,
    address_state TEXT,
    address_zipcode TEXT,
    loginAttempts INTEGER NOT NULL DEFAULT 0,
    isLocked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contactNumber_supplier (
    supplierID INTEGER NOT NULL,
    number TEXT NOT NULL,
    PRIMARY KEY (supplierID, number),
    FOREIGN KEY (supplierID) REFERENCES supplier(supplierID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS supplies (
    supplierID INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    offerPrice REAL NOT NULL DEFAULT 0 CHECK (offerPrice >= 0),
    PRIMARY KEY (supplierID, productID),
    FOREIGN KEY (supplierID) REFERENCES supplier(supplierID) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cart (
    customerID INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (customerID, productID),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_product_name ON product(name);
CREATE INDEX IF NOT EXISTS idx_product_category ON product(categoryID);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customerID);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(orderStatus);
"""


SEED_SQL = """
INSERT OR IGNORE INTO customer
(customerID, age, date_of_birth, name_first, name_middle, name_last, username, password, gender)
VALUES
(1, 25, '1999-05-15', 'John', 'Doe', 'Smith', 'john_doe', 'password123', 'M'),
(2, 30, '1994-10-20', 'Emily', 'Anne', 'Johnson', 'emily_j', 'securepass', 'F'),
(3, 40, '1984-03-10', 'Michael', NULL, 'Brown', 'mikebrown', '123456', 'M');

INSERT OR IGNORE INTO customerProfile
(customerID, address_street_name, address_street_number, address_city, address_state, address_zipcode, payment)
VALUES
(1, 'Main Street', '123', 'New York', 'NY', '10001', 'Credit Card'),
(2, 'Elm Street', '456', 'Los Angeles', 'CA', '90001', 'PayPal'),
(3, 'Oak Street', '789', 'Chicago', 'IL', '60001', 'Cash');

INSERT OR IGNORE INTO contactNumber_customer (customerID, number)
VALUES
(1, '123-456-7890'),
(1, '987-654-3210'),
(2, '555-555-5555'),
(3, '777-777-7777');

INSERT OR IGNORE INTO admin
(adminID, name_first, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES
(1, 'Admin', '', 'Smith', 'admin1', 'adminpass', 'Admin Street', '1', 'Admin City', 'Admin State', '12345'),
(2, 'Sarah', 'Elizabeth', 'Brown', 'sarah_b', 'admin123', 'Admin Boulevard', '3', 'Adminville', 'Admin State', '54321');

INSERT OR IGNORE INTO contactNumber_admin (adminID, number)
VALUES
(1, '111-111-1111'),
(1, '222-222-2222'),
(2, '333-111-2222');

INSERT OR IGNORE INTO supplier
(supplierID, name_first, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES
(1, 'North', '', 'Books', 'supplier1', 'supplierpass', 'Supplier Street', '123', 'Supplier City', 'Supplier State', '11111');

INSERT OR IGNORE INTO contactNumber_supplier (supplierID, number)
VALUES
(1, '333-333-3333');

INSERT OR IGNORE INTO productCategory (categoryID, name, description)
VALUES
(1, 'Books', 'Literature, technical books, and non-fiction'),
(2, 'Stationery', 'Reading and writing accessories');

INSERT OR IGNORE INTO manages (adminID, categoryID)
VALUES
(1, 1),
(2, 2);

INSERT OR IGNORE INTO product
(productID, description, quantityAvailable, price, name, review, categoryID)
VALUES
(101, 'A classic fantasy novel', 6, 15, 'The Lord of the Rings', 'Excellent', 1),
(102, 'Clean Code by Robert C. Martin', 10, 38, 'Clean Code', 'Great', 1),
(103, 'Hardcover notebook', 25, 8, 'Reading Journal', 'Good', 2);

INSERT OR IGNORE INTO supplies (supplierID, productID, quantity, offerPrice)
VALUES
(1, 101, 20, 11),
(1, 102, 10, 31);
"""


def initialize_sqlite(connection: Any, seed: bool = True) -> None:
    connection.executescript(SCHEMA_SQL)
    if seed:
        connection.executescript(SEED_SQL)
    connection.commit()
