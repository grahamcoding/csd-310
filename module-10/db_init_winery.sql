/*
    Title: db_init_winery.sql
    Authors: Stephanie Ramos, Aidan Jacoby, Daniel Graham
    Date: 11 Jul 2025
    Description: Bacchus Winery Case Study initialization script.
*/

-- drop database user if exists 
DROP USER IF EXISTS 'winery_user'@'localhost';
DROP DATABASE IF EXISTS winery;


-- create winery_user and grant them all privileges to the winery database 
CREATE USER 'winery_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'grapes';
CREATE DATABASE winery;
USE winery;

-- grant all privileges to the winery database to user winery_user on localhost 
GRANT ALL PRIVILEGES ON winery.* TO 'winery_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS Wine_Order_Item;
DROP TABLE IF EXISTS Wine_Order;
DROP TABLE IF EXISTS Wine_Distribution;
DROP TABLE IF EXISTS Wine;
DROP TABLE IF EXISTS Supply_Delivery;
DROP TABLE IF EXISTS Supply;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Work_Hours;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Distributor;

-- create the Department table 
CREATE TABLE Department (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

-- create the Emloyee table and set the foreign key
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- create the work_hours table and set the foreign key
CREATE TABLE Work_Hours (
    work_hours_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    year YEAR NOT NULL,
    quarter INT CHECK (quarter BETWEEN 1 AND 4),
    hours_worked INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- create the Supplier table
CREATE TABLE Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100)
);

-- create the Supply table and set the foreign key
CREATE TABLE Supply (
    supply_id INT AUTO_INCREMENT PRIMARY KEY,
    supply_name VARCHAR(100) NOT NULL,
    supplier_id INT NOT NULL,
    category VARCHAR(50),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- create Supply delivery table and set the foreign key
CREATE TABLE Supply_Delivery (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    supply_id INT NOT NULL,
    expected_delivery DATE NOT NULL,
    actual_delivery DATE NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (supply_id) REFERENCES Supply(supply_id)
);

-- create the Wine table
CREATE TABLE Wine (
    wine_id INT AUTO_INCREMENT PRIMARY KEY,
    wine_name VARCHAR(50) NOT NULL,
    grape_type VARCHAR(50),
    year YEAR
);

-- create the Distributor table
CREATE TABLE Distributor (
    distributor_id INT AUTO_INCREMENT PRIMARY KEY,
    distributor_name VARCHAR(100),
    contact_info VARCHAR(100)
);

-- Create the Wine distribution table and set the foreign key
CREATE TABLE Wine_Distribution (
    distribution_id INT AUTO_INCREMENT PRIMARY KEY,
    wine_id INT NOT NULL,
    distributor_id INT NOT NULL,
    distribution_date DATE,
    quantity INT,
    FOREIGN KEY (wine_id) REFERENCES Wine(wine_id),
    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
);

-- create the Wine order table and set the foreign key
CREATE TABLE Wine_Order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    distributor_id INT NOT NULL,
    order_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
);

-- create the Wine order item table and set foreign keys
CREATE TABLE Wine_Order_Item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    wine_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Wine_Order(order_id),
    FOREIGN KEY (wine_id) REFERENCES Wine(wine_id)
);

-- Sample data inserts

-- Departments
INSERT INTO Department (department_name) VALUES ('Finance'), ('Marketing'), ('Production'), ('Distribution');

-- Employees
INSERT INTO Employee (first_name, last_name, position, department_id)
VALUES 
    ('Janet', 'Collins', 'Finance Manager', 1),
    ('Roz', 'Murphy', 'Marketing Head', 2),
    ('Bob', 'Ulrich', 'Marketing Assistant', 2),
    ('Henry', 'Doyle', 'Production Manager', 3),
    ('Maria', 'Costanza', 'Distribution Manager', 4);

-- Wines
INSERT INTO Wine (wine_name, grape_type, year) VALUES
    ('Merlot SQL', 'Merlot', 2025),
    ('Cabernet SQL', 'Cabernet', 2025),
    ('Chablis SQL', 'Chablis', 2025),
    ('Chardonnay SQL', 'Chardonnay', 2025);

-- Suppliers
INSERT INTO Supplier (supplier_name, contact_info) VALUES
    ('Bottles and Corks Co.', 'bottles@example.com'),
    ('Labels and Boxes Ltd.', 'label@example.com'),
    ('Tubes and Vats Brothers', 'tubes@example.com');

-- Supplies
INSERT INTO Supply (supply_name, supplier_id, category) VALUES
    ('Bottles', 1, 'Packaging'),
    ('Corks', 1, 'Packaging'),
    ('Labels', 2, 'Packaging'),
    ('Boxes', 2, 'Packaging'),
    ('Vats', 3, 'Equipment'),
    ('Tubing', 3, 'Equipment');
    
    -- Work Hours (quarterly for a year)
INSERT INTO Work_Hours (employee_id, year, quarter, hours_worked) VALUES
    (1, 2024, 1, 480), (1, 2024, 2, 500), (1, 2024, 3, 510), (1, 2024, 4, 495),
    (2, 2024, 1, 460), (2, 2024, 2, 470),
    (3, 2024, 1, 450), (3, 2024, 2, 455),
    (4, 2024, 1, 600), (4, 2024, 2, 610),
    (5, 2024, 1, 520), (5, 2024, 2, 530);

-- Supply Deliveries
INSERT INTO Supply_Delivery (supply_id, expected_delivery, actual_delivery, quantity) VALUES
    (1, '2025-01-01', '2025-01-03', 1000),
    (2, '2025-01-01', '2025-01-01', 500),
    (3, '2025-01-05', '2025-01-10', 700),
    (4, '2025-01-05', '2025-01-07', 300),
    (5, '2025-01-10', '2025-01-15', 2),
    (6, '2025-01-10', '2025-01-10', 50);

-- Distributors
INSERT INTO Distributor (distributor_name, contact_info) VALUES
    ('Midwest Wines', 'midwest@example.com'),
    ('East Coast Wines', 'eastcoast@example.com'),
    ('West Coast Wines', 'westcoast@example.com'),
    ('Northern Wines', 'northern@example.com'),
    ('Southern Wines', 'southern@example.com'),
    ('Exported Wines', 'exports@example.com');

-- Wine Distribution
INSERT INTO Wine_Distribution (wine_id, distributor_id, distribution_date, quantity) VALUES
    (1, 1, '2025-06-01', 100),
    (2, 2, '2025-06-01', 200),
    (3, 3, '2025-06-01', 150),
    (4, 4, '2025-06-01', 180),
    (1, 5, '2025-06-02', 75),
    (2, 6, '2025-06-02', 125);

-- Wine Orders
INSERT INTO Wine_Order (distributor_id, order_date, status) VALUES
    (1, '2025-06-01', 'Shipped'),
    (2, '2025-06-01', 'Delivered'),
    (3, '2025-06-02', 'Processing'),
    (4, '2025-06-02', 'Shipped'),
    (5, '2025-06-03', 'Delivered'),
    (6, '2025-06-03', 'Pending');

-- Wine Order Items
INSERT INTO Wine_Order_Item (order_id, wine_id, quantity) VALUES
    (1, 1, 50),
    (1, 2, 25),
    (2, 2, 100),
    (3, 3, 75),
    (4, 4, 60),
    (5, 1, 90),
    (6, 4, 40);