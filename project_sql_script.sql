-- Project SQL Initialization Script

CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Vendors Table
CREATE TABLE vendors (
    vendor_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    rating DECIMAL(3,2) CHECK (rating BETWEEN 0 AND 5),
    location VARCHAR(50)
);

-- Products Table
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    tags VARCHAR(255),
    vendor_id VARCHAR(20),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    shipping_address TEXT
);

-- Orders Table
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    status ENUM('pending', 'shipped', 'cancelled'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
    order_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INT CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sample Data
INSERT INTO vendors VALUES
('V001', 'Tech World', 4.5, 'Hong Kong'),
('V002', 'Fashion Hub', 4.2, 'Shenzhen'),
('V003', 'Home Essentials', 4.8, 'Guangzhou'),
('V004', 'Digital Zone', 4.3, 'Shanghai'),
('V005', 'Beauty Corner', 4.6, 'Beijing'),
('V006', 'Sports Elite', 4.4, 'Chengdu'),
('V007', 'Book Haven', 4.1, 'Wuhan'),
('V008', 'Baby Care Plus', 4.7, 'Nanjing'),
('V009', 'Auto Parts Pro', 4.0, 'Tianjin'),
('V010', 'Kitchen Master', 4.5, 'Hangzhou');

INSERT INTO products VALUES
('P1001', 'Wireless Mouse', 59.99, 'electronics,computer', 'V001'),
('P1002', 'Bluetooth Speaker', 199.99, 'audio,electronics', 'V001'),
('P1003', 'Gaming Keyboard', 299.99, 'electronics,gaming', 'V001'),
('P1004', 'Summer Dress', 89.99, 'clothing,fashion', 'V002'),
('P1005', 'Leather Bag', 159.99, 'accessories,fashion', 'V002'),
('P1006', 'Smart Watch', 399.99, 'electronics,wearable', 'V004'),
('P1007', 'Yoga Mat', 45.99, 'sports,fitness', 'V006'),
('P1008', 'Baby Stroller', 299.99, 'baby,gear', 'V008'),
('P1009', 'Car Phone Holder', 25.99, 'auto,accessories', 'V009'),
('P1010', 'Coffee Maker', 129.99, 'kitchen,appliances', 'V010');

INSERT INTO customers VALUES
('C001', '13800138001', 'Beijing Chaoyang District'),
('C002', '13800138002', 'Shanghai Pudong New Area'),
('C003', '13800138003', 'Guangzhou Tianhe District'),
('C004', '13800138004', 'Shenzhen Nanshan District'),
('C005', '13800138005', 'Hangzhou West Lake District'),
('C006', '13800138006', 'Chengdu High-tech Zone'),
('C007', '13800138007', 'Wuhan Wuchang District'),
('C008', '13800138008', 'Nanjing Xianlin University Town'),
('C009', '13800138009', 'Tianjin Binhai New Area'),
('C010', '13800138010', 'Xi\'an Hi-tech Industries Zone');

INSERT INTO orders VALUES
('O001', 'C001', 'pending'),
('O002', 'C002', 'shipped'),
('O003', 'C003', 'pending'),
('O004', 'C004', 'cancelled'),
('O005', 'C005', 'shipped');

INSERT INTO order_items VALUES
('O001', 'P1001', 2),
('O001', 'P1002', 1),
('O002', 'P1004', 1),
('O003', 'P1006', 1),
('O004', 'P1008', 1),
('O005', 'P1010', 2);