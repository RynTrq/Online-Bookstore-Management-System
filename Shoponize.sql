-- Shoponize production-ready MySQL schema and seed data.
-- Safe to run repeatedly in a local development database.

CREATE DATABASE IF NOT EXISTS shoponize
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE shoponize;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS supplies;
DROP TABLE IF EXISTS contains;
DROP TABLE IF EXISTS contactNumber_supplier;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS contactNumber_admin;
DROP TABLE IF EXISTS manages;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS productCategory;
DROP TABLE IF EXISTS customerProfile;
DROP TABLE IF EXISTS contactNumber_customer;
DROP TABLE IF EXISTS customer;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE customer (
    customerID INT PRIMARY KEY,
    age INT CHECK (age IS NULL OR age >= 0),
    date_of_birth DATE,
    name_first VARCHAR(100),
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender CHAR(1) NOT NULL,
    loginAttempts INT NOT NULL DEFAULT 0,
    isLocked BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE contactNumber_customer (
    customerID INT NOT NULL,
    number VARCHAR(20) NOT NULL,
    PRIMARY KEY (customerID, number),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE
);

CREATE TABLE customerProfile (
    customerID INT PRIMARY KEY,
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    payment VARCHAR(100),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE
);

CREATE TABLE productCategory (
    categoryID INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE product (
    productID INT PRIMARY KEY,
    description VARCHAR(255),
    quantityAvailable INT NOT NULL DEFAULT 0 CHECK (quantityAvailable >= 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    name VARCHAR(100) NOT NULL,
    review VARCHAR(50),
    categoryID INT,
    isLowStock BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID) ON DELETE SET NULL,
    INDEX idx_product_name (name),
    INDEX idx_product_category (categoryID)
);

CREATE TABLE orders (
    orderNumber INT PRIMARY KEY,
    customerID INT NOT NULL,
    orderDate DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    orderStatus VARCHAR(50) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE,
    INDEX idx_orders_customer (customerID),
    INDEX idx_orders_status (orderStatus)
);

CREATE TABLE contains (
    orderNumber INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unitPrice DECIMAL(10, 2) NOT NULL CHECK (unitPrice >= 0),
    PRIMARY KEY (orderNumber, productID),
    FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE RESTRICT
);

CREATE TABLE admin (
    adminID INT PRIMARY KEY,
    name_first VARCHAR(100),
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    loginAttempts INT NOT NULL DEFAULT 0,
    isLocked BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE contactNumber_admin (
    adminID INT NOT NULL,
    number VARCHAR(20) NOT NULL,
    PRIMARY KEY (adminID, number),
    FOREIGN KEY (adminID) REFERENCES admin(adminID) ON DELETE CASCADE
);

CREATE TABLE manages (
    adminID INT NOT NULL,
    categoryID INT NOT NULL,
    PRIMARY KEY (adminID, categoryID),
    FOREIGN KEY (adminID) REFERENCES admin(adminID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID) ON DELETE CASCADE
);

CREATE TABLE supplier (
    supplierID INT PRIMARY KEY,
    name_first VARCHAR(100),
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    loginAttempts INT NOT NULL DEFAULT 0,
    isLocked BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE contactNumber_supplier (
    supplierID INT NOT NULL,
    number VARCHAR(20) NOT NULL,
    PRIMARY KEY (supplierID, number),
    FOREIGN KEY (supplierID) REFERENCES supplier(supplierID) ON DELETE CASCADE
);

CREATE TABLE supplies (
    supplierID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    offerPrice DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (offerPrice >= 0),
    PRIMARY KEY (supplierID, productID),
    FOREIGN KEY (supplierID) REFERENCES supplier(supplierID) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE CASCADE
);

CREATE TABLE cart (
    customerID INT NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (customerID, productID),
    FOREIGN KEY (customerID) REFERENCES customer(customerID) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE CASCADE
);

INSERT INTO customer
(customerID, age, date_of_birth, name_first, name_middle, name_last, username, password, gender)
VALUES
(1, 25, '1999-05-15', 'John', 'Doe', 'Smith', 'john_doe', 'password123', 'M'),
(2, 30, '1994-10-20', 'Emily', 'Anne', 'Johnson', 'emily_j', 'securepass', 'F'),
(3, 40, '1984-03-10', 'Michael', NULL, 'Brown', 'mikebrown', '123456', 'M');

INSERT INTO customerProfile
(customerID, address_street_name, address_street_number, address_city, address_state, address_zipcode, payment)
VALUES
(1, 'Main Street', '123', 'New York', 'NY', '10001', 'Credit Card'),
(2, 'Elm Street', '456', 'Los Angeles', 'CA', '90001', 'PayPal'),
(3, 'Oak Street', '789', 'Chicago', 'IL', '60001', 'Cash');

INSERT INTO contactNumber_customer (customerID, number)
VALUES
(1, '123-456-7890'),
(1, '987-654-3210'),
(2, '555-555-5555'),
(3, '777-777-7777');

INSERT INTO productCategory (categoryID, name, description)
VALUES
(1, 'Books', 'Literature, technical books, and non-fiction'),
(2, 'Stationery', 'Reading and writing accessories');

INSERT INTO product
(productID, description, quantityAvailable, price, name, review, categoryID)
VALUES
(101, 'A classic fantasy novel', 6, 15.00, 'The Lord of the Rings', 'Excellent', 1),
(102, 'Clean Code by Robert C. Martin', 10, 38.00, 'Clean Code', 'Great', 1),
(103, 'Hardcover notebook', 25, 8.00, 'Reading Journal', 'Good', 2);

INSERT INTO orders (orderNumber, customerID, orderDate, amount, orderStatus)
VALUES
(1000, 1, '2024-03-15', 53.00, 'Delivered');

INSERT INTO contains (orderNumber, productID, quantity, unitPrice)
VALUES
(1000, 101, 1, 15.00),
(1000, 102, 1, 38.00);

INSERT INTO admin
(adminID, name_first, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES
(1, 'Admin', '', 'Smith', 'admin1', 'adminpass', 'Admin Street', '1', 'Admin City', 'Admin State', '12345'),
(2, 'Sarah', 'Elizabeth', 'Brown', 'sarah_b', 'admin123', 'Admin Boulevard', '3', 'Adminville', 'Admin State', '54321');

INSERT INTO contactNumber_admin (adminID, number)
VALUES
(1, '111-111-1111'),
(1, '222-222-2222'),
(2, '333-111-2222');

INSERT INTO manages (adminID, categoryID)
VALUES
(1, 1),
(2, 2);

INSERT INTO supplier
(supplierID, name_first, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES
(1, 'North', '', 'Books', 'supplier1', 'supplierpass', 'Supplier Street', '123', 'Supplier City', 'Supplier State', '11111');

INSERT INTO contactNumber_supplier (supplierID, number)
VALUES
(1, '333-333-3333');

INSERT INTO supplies (supplierID, productID, quantity, offerPrice)
VALUES
(1, 101, 20, 11.00),
(1, 102, 10, 31.00);
