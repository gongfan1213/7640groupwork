"""
Main Application Module
Command-line interface for e-commerce platform
"""
from vendor_mgmt import display_vendors, add_new_vendor
from product_catalog import browse_vendor_products, add_new_product
from search_engine import search_by_tags
from order_system import OrderSystem

def main_menu():
    """Display main menu and handle user input"""
    while True:
        print("\n=== E-Commerce Platform ===")
        print("1. Vendor Management")
        print("2. Product Catalog")
        print("3. Product Search")
        print("4. Order Management")
        print("5. Exit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            vendor_management_menu()
        elif choice == '2':
            product_catalog_menu()
        elif choice == '3':
            search_menu()
        elif choice == '4':
            order_management_menu()
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid choice, please try again")

def vendor_management_menu():
    """Handle vendor-related operations"""
    while True:
        print("\n=== Vendor Management ===")
        print("1. List All Vendors")
        print("2. Add New Vendor")
        print("3. Return to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            display_vendors()
        elif choice == '2':
            add_new_vendor()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

# 类似实现其他子菜单函数

def generate_sql_script():
    """Generate SQL initialization script"""
    sql_content = """
-- Group X SQL Initialization Script

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
('V002', 'Fashion Hub', 4.2, 'Shenzhen');

INSERT INTO products VALUES
('P1001', 'Wireless Mouse', 59.99, 'electronics,computer', 'V001'),
('P1002', 'Bluetooth Speaker', 199.99, 'audio,electronics', 'V001');
"""
    with open('groupX_insert_sql.txt', 'w') as f:
        f.write(sql_content)

if __name__ == "__main__":
    generate_sql_script()
    main_menu()