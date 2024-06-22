CREATE DATABASE shoponize;

USE shoponize;

CREATE TABLE customer (
    customerID INT PRIMARY KEY,
    age INT,
    date_of_birth DATE,
    name_first VARCHAR(100),
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255),
    password VARCHAR(255),
    gender char(1) NOT NULL,
    loginAttempts INT DEFAULT 0,
    isLocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE contactNumber_customer (
	customerID INT,
    number VARCHAR(20),
	PRIMARY KEY(customerID,number),
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

CREATE TABLE customerProfile (
	customerID INT PRIMARY KEY,
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    payment VARCHAR(100),
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

CREATE TABLE `order`(
    orderNumber INT PRIMARY KEY,
    customerID INT NOT NULL,
    orderDate DATE,
    AMOUNT INT,
    orderStatus VARCHAR(50),
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
);

CREATE TABLE productCategory(
	categoryID INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(100)
);

CREATE TABLE product(
	productID INT PRIMARY KEY,
    description VARCHAR(100),
    quantityAvailable INT,
    price INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    review VARCHAR(20),
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID),
    isLowStock BOOLEAN DEFAULT FALSE
);

CREATE TABLE contains(
	orderNumber INT NOT NULL,
    productID INT NOT NULL,
    PRIMARY KEY(orderNumber, productID),
    FOREIGN KEY (orderNumber) REFERENCES `order`(orderNumber),
    FOREIGN KEY (productID) REFERENCES product(productID)
);

CREATE TABLE admin(
	adminID INT PRIMARY KEY,
    name_first VARCHAR(100),
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255),
    password VARCHAR(255),
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    loginAttempts INT DEFAULT 0,
    isLocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE contactNumber_admin(
	adminID INT,
    number VARCHAR(20),
    PRIMARY KEY(adminID, number),
    FOREIGN KEY (adminID) REFERENCES admin(adminID)
);

CREATE TABLE manages(
	adminID INT NOT NULL,
    categoryID INT NOT NULL,
    FOREIGN KEY (adminID) REFERENCES admin(adminID),
    FOREIGN KEY (categoryID) REFERENCES productCategory(categoryID)
);

CREATE TABLE supplier(
	supplierID INT PRIMARY KEY,
    name_middle VARCHAR(100),
    name_last VARCHAR(100),
    username VARCHAR(255),
    password VARCHAR(255),
    address_street_name VARCHAR(255),
    address_street_number VARCHAR(50),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_zipcode VARCHAR(20),
    loginAttempts INT DEFAULT 0,
    isLocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE contactNumber_supplier(
    supplierID INT,
    number VARCHAR(20),
    PRIMARY KEY (supplierID, number),
    FOREIGN KEY (supplierID) REFERENCES supplier(supplierID)
);

CREATE TABLE supplies(
	supplierID INT,
    productID INT,
    PRIMARY KEY(supplierID, productID),
    FOREIGN KEY(supplierID) REFERENCES supplier(supplierID),
    FOREIGN KEY(productID) REFERENCES product(productID)
);

CREATE TABLE cart(
	customerID INT,
    productID INT,
    quantity INT,
    PRIMARY KEY(customerID,productID),
    FOREIGN KEY(customerID) REFERENCES customer(customerID),
    FOREIGN KEY(productID) REFERENCES product(productID)
);

-- Sample data for customer table
INSERT INTO customer (customerID, age, date_of_birth, name_first, name_middle, name_last, username, password, gender)
VALUES 
(1, 25, '1999-05-15', 'John', 'Doe', 'Smith', 'john_doe', 'password123', 'M'),
(2, 30, '1994-10-20', 'Emily', 'Anne', 'Johnson', 'emily_j', 'securepass', 'F'),
(3, 40, '1984-03-10', 'Michael', null , 'Brown', 'mikebrown', '123456', 'M'),
(4, 22, '2002-08-10', 'Emma', 'Rose', 'Davis', 'emma_davis', 'pass123', 'F'),
(5, 35, '1989-04-25', 'David', 'Lee', 'Wilson', 'david_w', 'securepassword', 'M'),
(6, 28, '1996-11-15', 'Sophia', 'Grace', 'Taylor', 'sophia_t', 'password321', 'F'),
(7, 45, '1979-09-05', 'Matthew', 'John', 'Anderson', 'matt_anderson', 'abc123', 'M'),
(8, 31, '1993-07-20', 'Olivia', 'Mae', 'Robinson', 'olivia_r', 'qwerty', 'F'),
(9, 29, '1995-12-18', 'Ethan', 'Michael', 'Brown', 'ethan_brown', 'pass123', 'M'),
(10, 26, '1998-09-22', 'Ava', 'Nicole', 'Martinez', 'ava_m', 'securepass', 'F'),
(11, 33, '1991-07-14', 'Sophie', 'Elizabeth', 'Garcia', 'sophie_g', 'password321', 'F'),
(12, 27, '1997-04-05', 'James', 'Alexander', 'Hernandez', 'james_h', 'abc123', 'M'),
(13, 40, '1984-02-28', 'Ella', 'Grace', 'Scott', 'ella_s', 'qwerty', 'F'),
(14, 22, '2002-01-10', 'Noah', 'William', 'King', 'noah_k', 'adminpass', 'M'),
(15, 38, '1986-11-30', 'Isabella', 'Madison', 'Young', 'isabella_y', 'pass123', 'F');

-- Sample data for contactNumber_customer table
INSERT INTO contactNumber_customer (customerID, number)
VALUES 
(1, '123-456-7890'),
(1, '987-654-3210'),
(2, '555-555-5555'),
(3, '777-777-7777'),
(4, '555-123-4567'),
(4, '999-888-7777'),
(5, '999-888-7777'),
(6, '111-222-3333'),
(7, '444-555-6666'),
(8, '777-888-9999'),
(9, '555-333-4444'),
(10, '111-222-3333'),
(11, '777-999-8888'),
(12, '444-555-6666'),
(13, '123-456-7890'),
(14, '999-888-7777'),
(15, '777-666-5555');

-- Sample data for customerProfile table
INSERT INTO customerProfile (customerID, address_street_name, address_street_number, address_city, address_state, address_zipcode, payment)
VALUES 
(1, 'Main Street', '123', 'New York', 'NY', '10001', 'Credit Card'),
(2, 'Elm Street', '456', 'Los Angeles', 'CA', '90001', 'PayPal'),
(3, 'Oak Street', '789', 'Chicago', 'IL', '60001', 'Cash'),
(4, 'Park Avenue', '456', 'San Francisco', 'CA', '94101', 'Credit Card'),
(5, 'Maple Street', '789', 'Seattle', 'WA', '98101', 'PayPal'),
(6, 'Cedar Lane', '123', 'Boston', 'MA', '02101', 'Credit Card'),
(7, 'Pine Street', '789', 'Miami', 'FL', '33101', 'Cash'),
(8, 'Elm Avenue', '456', 'Denver', 'CO', '80123', 'Credit Card'),
(9, 'Oak Avenue', '123', 'Chicago', 'IL', '60601', 'Credit Card'),
(10, 'Chestnut Street', '456', 'Houston', 'TX', '77001', 'PayPal'),
(11, 'Walnut Lane', '789', 'Philadelphia', 'PA', '19101', 'Credit Card'),
(12, 'Cedar Street', '456', 'Phoenix', 'AZ', '85001', 'Cash'),
(13, 'Pine Avenue', '789', 'San Antonio', 'TX', '78201', 'Credit Card'),
(14, 'Maple Lane', '123', 'San Diego', 'CA', '92101', 'PayPal'),
(15, 'Elm Street', '456', 'Dallas', 'TX', '75201', 'Credit Card');

-- Sample data for order table
INSERT INTO `order` (orderNumber, customerID, orderDate, AMOUNT, orderStatus)
VALUES 
(1001, 1, '2024-03-15', 150, 'Delivered'),
(1002, 2, '2024-03-20', 200, 'In Progress'),
(1003, 3, '2024-03-25', 100, 'Pending'),
(1004, 4, '2024-03-28', 75, 'Delivered'),
(1005, 5, '2024-03-30', 150, 'In Progress'),
(1006, 6, '2024-03-29', 100, 'Pending'),
(1007, 7, '2024-03-27', 200, 'Delivered'),
(1008, 8, '2024-03-26', 125, 'In Progress'),
(1009, 9, '2024-03-30', 100, 'Pending'),
(1010, 10, '2024-03-31', 75, 'Delivered'),
(1011, 11, '2024-03-29', 200, 'In Progress'),
(1012, 12, '2024-03-28', 150, 'Delivered'),
(1013, 13, '2024-03-27', 125, 'In Progress'),
(1014, 14, '2024-03-26', 100, 'Delivered'),
(1015, 15, '2024-03-25', 80, 'Pending');

-- Sample data for productCategory table
INSERT INTO productCategory (categoryID, name, description)
VALUES 
(1, 'Electronics', 'Electronic devices and gadgets'),
(2, 'Clothing', 'Apparel and fashion accessories'),
(3, 'Home & Kitchen', 'Household items and kitchenware'),
(4, 'Books', 'Literature and non-fiction books'),
(5, 'Beauty', 'Cosmetics and skincare products'),
(6, 'Sports & Outdoors', 'Equipment and gear for outdoor activities'),
(7, 'Toys & Games', 'Children\'s toys and games'),
(8, 'Food & Beverage', 'Groceries and beverages'),
(9, 'Health & Wellness', 'Vitamins and supplements');

-- Sample data for product table
INSERT INTO product (productID, description, price, name, review, categoryID,quantityAvailable)
VALUES 
(101, 'Smartphone', 500, 'iPhone 13', 'Good', 1,12),
(102, 'Laptop', 1000, 'Macbook Pro', 'Excellent', 1,10),
(103, 'T-shirt', 20, 'Plain White Tee', 'Average', 2,15),
(104, 'Jeans', 50, 'Blue Denim Jeans', 'Great', 2,4),
(105, 'Coffee Maker', 50, 'Drip Coffee Machine', 'Excellent', 3,35),
(106, 'Fantasy Novel', 15, 'The Lord of the Rings', 'Excellent', 4,6),
(107, 'Foundation', 30, 'Liquid Foundation', 'Great', 5,7),
(108, 'Yoga Mat', 25, 'Eco-Friendly Yoga Mat', 'Good', 6,23),
(109, 'Running Shoes', 80, 'Nike Air Zoom', 'Excellent', 6,36),
(110, 'Eyeshadow Palette', 40, 'Urban Decay Naked Palette', 'Average', 5,9),
(111, 'Board Game', 30, 'Settlers of Catan', 'Excellent', 7,4),
(112, 'Coffee Beans', 10, 'Organic Arabica Coffee', 'Good', 8,17),
(113, 'Multivitamin', 20, 'Nature Way Alive!', 'Excellent', 9,20),
(114, 'LEGO Set', 50, 'LEGO Creator Expert', 'Great', 7,10),
(115, 'Chocolate Bar', 5, 'Dark Chocolate Bar', 'Good', 8,20),
(116, 'Protein Powder', 25, 'Optimum Nutrition Gold Standard', 'Excellent', 9,13);

-- Sample data for contains table
INSERT INTO contains (orderNumber, productID)
VALUES 
(1001, 101),
(1001, 104),
(1002, 102),
(1003, 105),
(1004, 106),
(1005, 107),
(1005, 109),
(1006, 108),
(1007, 109),
(1007, 110),
(1008, 107),
(1008, 108),
(1009, 111),
(1010, 112),
(1010, 113),
(1011, 114),
(1012, 115),
(1013, 116),
(1014, 111),
(1015, 112);


-- Sample data for admin table
INSERT INTO admin (adminID, name_first, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES 
(1, 'Admin', '', 'Smith', 'admin1', 'adminpass', 'Admin Street', '1', 'Admin City', 'Admin State', '12345'),
(2, 'Admin', '', 'Johnson', 'admin2', 'adminpass', 'Admin Road', '2', 'Admin Town', 'Admin State', '54321'),
(3, 'Sarah', 'Elizabeth', 'Brown', 'sarah_b', 'admin123', 'Admin Boulevard', '3', 'Adminville', 'Admin State', '54321'),
(4, 'Robert', 'James', 'Miller', 'rob_m', 'admin123', 'Admin Lane', '4', 'Admin City', 'Admin State', '12345'),
(5, 'Emma', 'Louise', 'Wilson', 'emma_w', 'admin123', 'Admin Street', '5', 'Admin City', 'Admin State', '54321'),
(6, 'Daniel', 'Joseph', 'Clark', 'daniel_c', 'admin123', 'Admin Road', '6', 'Adminville', 'Admin State', '12345');


-- Sample data for contactNumber_admin table
INSERT INTO contactNumber_admin (adminID, number)
VALUES 
(1, '111-111-1111'),
(1, '222-222-2222'),
(2, '333-111-2222'),
(2, '444-555-6666'),
(3, '333-111-2222'),
(4, '444-555-6666'),
(5, '222-333-4444'),
(5, '555-666-7777'),
(6, '222-333-4444'),
(6, '555-666-7777');

-- Sample data for manages table
INSERT INTO manages (adminID, categoryID)
VALUES 
(1, 1),
(2, 2),
(3, 4),
(3, 5),
(4, 6),
(5, 7),
(5, 8),
(6, 9);


-- Sample data for supplier table
INSERT INTO supplier (supplierID, name_middle, name_last, username, password, address_street_name, address_street_number, address_city, address_state, address_zipcode)
VALUES 
(1, '', 'Supplier1', 'supplier1', 'supplierpass', 'Supplier Street', '123', 'Supplier City', 'Supplier State', '11111'),
(2, '', 'Supplier2', 'supplier2', 'supplierpass', 'Supplier Road', '456', 'Supplier Town', 'Supplier State', '22222'),
(3, '', 'Supplier3', 'supplier3', 'supplierpass', 'Supplier Avenue', '789', 'Supplier Town', 'Supplier State', '33333'),
(4, '', 'Supplier4', 'supplier4', 'supplierpass', 'Supplier Circle', '987', 'Supplier City', 'Supplier State', '44444'),
(5, '', 'Supplier5', 'supplier5', 'supplierpass', 'Supplier Boulevard', '123', 'Supplier City', 'Supplier State', '55555'),
(6, '', 'Supplier6', 'supplier6', 'supplierpass', 'Supplier Lane', '456', 'Supplier Town', 'Supplier State', '66666');

-- Sample data for contactNumber_supplier table
INSERT INTO contactNumber_supplier (supplierID, number)
VALUES 
(1, '333-333-3333'),
(1, '777-888-9999'),
(2, '444-444-4444'),
(2, '888-999-0000'),
(3, '777-888-9999'),
(4, '999-000-1111'),
(4, '000-111-2222'),
(5, '999-000-1111'),
(5, '000-111-2222'),
(6, '999-000-1111'),
(6, '000-111-2222');

-- Sample data for supplies table
INSERT INTO supplies (supplierID, productID)
VALUES 
(1, 101),
(2, 105),
(3, 106),
(4, 107),
(4, 108),
(3, 109),
(3, 110),
(5, 111),
(6, 112),
(6, 113),
(5, 114),
(6, 115),
(5, 116);


