# COMP7640 Multi-Vendor E-Commerce Platform Project Report

## 1. Team Members
(To be supplemented with specific member information)

## 2. System Design

### 2.1 ER Diagram Design
![image](https://github.com/user-attachments/assets/008b6d36-8d0c-492a-92f9-c3f9f1c9d011)
Our system design includes the following key entities:

#### Core Entities
- **Vendor**: Manages vendor information, including ID, name, rating, and location.
- **Product**: Records product information, including ID, name, price, and tags.
- **Customer**: Stores customer information, including ID, phone number, and shipping address.
- **Order**: Manages transaction records, including order status and creation time.
- **OrderItem**: Records order details, including products and quantities.
- **OrderLog**: Tracks order status changes.

#### Entity Relationships
- **Vendor and Product**: One-to-many relationship where one vendor can provide multiple products.
- **Customer and Order**: One-to-many relationship where one customer can place multiple orders.
- **Order and OrderItem**: One-to-many relationship where one order contains multiple order items.
- **Product and OrderItem**: Many-to-many relationship through the `OrderItem` table.
- **Order and OrderLog**: One-to-many relationship that tracks order status changes.

### 2.2 Database Table Design

#### vendors Table
- **vendor_id**: Vendor ID, primary key.
- **name**: Vendor name.
- **rating**: Rating (0-5 points).
- **location**: Vendor location.

#### products Table
- **product_id**: Product ID, primary key.
- **name**: Product name.
- **price**: Product price.
- **tags**: Product tags.
- **vendor_id**: Vendor ID, foreign key.

#### customers Table
- **customer_id**: Customer ID, primary key.
- **phone**: Contact phone number.
- **shipping_address**: Shipping address.

#### orders Table
- **order_id**: Order ID, primary key.
- **customer_id**: Customer ID, foreign key.
- **status**: Order status (pending/shipped/cancelled).
- **created_at**: Creation time.

#### order_items Table
- **order_id**: Order ID, composite primary key.
- **product_id**: Product ID, composite primary key.
- **quantity**: Quantity of the product.

#### order_logs Table
- **log_id**: Log ID, primary key.
- **order_id**: Order ID, foreign key.
- **action**: Type of operation.
- **details**: Detailed information.
- **log_time**: Log timestamp.

### 2.3 Normalization Explanation

The database design follows the Third Normal Form (3NF):
1. Each table has a primary key, meeting the first normal form.
2. Non-key fields fully depend on the primary key, meeting the second normal form.
3. No transitive dependency between non-key fields, meeting the third normal form.

## 3. Function Implementation

### 3.1 Vendor Management
- Display vendor list.
- Support vendor registration and information maintenance.
- Include vendor rating system.

### 3.2 Product Catalog Management
- Browse products by vendor.
- Add and update product information.
- Manage product tags.

### 3.3 Product Search Feature
- Search products by tags.
- Support fuzzy matching of product names.
- Optimize search response speed.

### 3.4 Order Management System
- Support ordering products from multiple vendors in a single order.
- Track order status.
- Support order modification and cancellation.

## 4. User Guide

### 4.1 Environment Requirements
- Python 3.5
- MySQL Database
- PyMySQL Package

### 4.2 Installation Steps
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the database:
   - Create a MySQL database.
   - Run `project_sql_script.sql` to initialize the database structure.

3. Start the application:
   ```bash
   python main.py
   ```

### 4.3 Usage Instructions
- **Vendor Management**: Implemented through the `vendor_mgmt.py` module.
- **Product Management**: Handled by the `product_catalog.py` module.
- **Order Operations**: Managed through the `order_system.py` module.
- **Search Function**: Implemented in the `search_engine.py` module.



## 5. Code Structure Explanation 

### 5.1 Database Connection Module (`db_conn.py`)

**Core Components:**
- `DBConnection` class encapsulates all database operations
- Uses PyMySQL library for MySQL connectivity
- Implements connection pooling pattern

**Key Methods:**
1. `connect()`:
   - Establishes connection to MySQL server on port 3307
   - Performs pre-connection check using socket to verify MySQL service availability
   - Configures connection with UTF-8MB4 charset for full Unicode support
   - Uses DictCursor for returning query results as dictionaries

2. `get_cursor()`:
   - Returns a database cursor with automatic connection verification
   - Implements lazy connection - only connects when first cursor is requested
   - Handles connection errors with specific error codes (1045 for auth failures)

3. Transaction Control:
   - `commit()`: Explicit commit operation
   - `rollback()`: Transaction rollback capability
   - Connection automatically closes when exiting context manager

**Error Handling:**
- Catches specific PyMySQL operational errors
- Provides human-readable messages for common errors:
  - 1045: Authentication failures
  - 1044: Permission issues
- Implements graceful fallback for connection failures

### 5.2 Data Models (`models.py`)

**Vendor Class:**
- Attributes: vendor_id, name, rating (0-5), location
- `save_to_db()` method:
  - Validates rating range before insertion
  - Uses parameterized queries to prevent SQL injection
  - Commits transaction explicitly

**Product Class:**
- Attributes: product_id, name, price (positive), tags (max 3), vendor_id
- `add_to_inventory()` method:
  - Enforces maximum 3 tags rule
  - Stores tags as comma-separated string
  - Validates price is positive
  - Maintains referential integrity with vendors

**Order Class:**
- Tracks order lifecycle states: pending → shipped/cancelled
- Manages line items collection
- Implements status transition validation
- Calculates order totals dynamically

### 5.3 Functional Modules

#### 5.3.1 Vendor Management (`vendor_mgmt.py`)

**Key Functions:**
1. `display_vendors()`:
   - Formats output in aligned columns
   - Handles large result sets with pagination
   - Shows rating as star symbols (★) for visual representation

2. `add_new_vendor()`:
   - Interactive CLI for data entry
   - Input validation for rating range
   - Auto-generates vendor IDs if not specified
   - Confirms successful registration

#### 5.3.2 Product Catalog (`product_catalog.py`)

**Core Features:**
- Paginated product browsing (`browse_vendor_products()`)
  - Calculates total pages dynamically
  - Implements next/previous page navigation
  - Shows product count statistics

- Product creation wizard (`add_new_product()`)
  - Tag input parsing and validation
  - Price formatting (HK$ prefix)
  - Vendor existence verification

#### 5.3.3 Search Engine (`search_engine.py`)

**Search Algorithm:**
- `search_by_tags()` performs:
  - Full-text search across name and tags fields
  - Case-insensitive pattern matching
  - Price-based sorting (asc/desc)
  - Vendor name joining for enriched results

**Result Formatting:**
- Highlights matching keywords
- Shows price with proper currency formatting
- Groups related products visually

#### 5.3.4 Order System (`order_system.py`)

**Order Lifecycle Management:**
1. Order Creation:
   - UUID-based order ID generation
   - Customer verification
   - Pending state initialization

2. Item Management:
   - Quantity validation (>0)
   - Product existence checking
   - Real-time subtotal calculation

3. State Transitions:
   - Pending → Shipped (with payment simulation)
   - Pending → Cancelled (with reason logging)
   - Prevents invalid transitions

**Advanced Features:**
- Order versioning through logs
- Bulk item operations
- Comprehensive order display with:
  - Customer details
  - Itemized breakdown
  - Grand total calculation

### 5.4 Main Program (`main.py`)

**UI System:**
- Hierarchical menu structure:
  - Main menu → Submenus → Operations
  - Consistent navigation pattern
  - Context-sensitive help

**Key Components:**
1. Menu Controllers:
   - Vendor management menu
   - Product catalog menu
   - Search interface
   - Order management console

2. SQL Script Generation:
   - Creates complete DDL with:
     - Table definitions
     - Constraints
     - Sample data
   - Outputs to `groupX_insert_sql.txt`

**Error Handling:**
- Graceful recovery from invalid inputs
- Transaction rollback on failures
- User-friendly error messages

**Integration:**
- Orchestrates all modules
- Maintains application state
- Implements cross-module workflows:
  - Vendor → Product → Order chain
  - Search → Add to cart flow

This architecture provides:
- Clear separation of concerns
- Reusable components
- Scalable foundation for enhancements
- Maintainable code organization

### 5.1 Database Connection Module (`db_conn.py`)
- Encapsulates MySQL connection operations.
- Provides connection management, transaction control, and cursor retrieval.
- Handles error management and connection status checking.

### 5.2 Data Models (`models.py`)
- `Vendor` Class: Manages vendor entity and database operations.
- `Product` Class: Manages product entity and inventory.
- `Customer` Class: Manages customer profiles.
- `Order` Class: Handles order lifecycle management.

### 5.3 Functional Modules
- **vendor_mgmt.py**: Vendor list display and registration.
- **product_catalog.py**: Product browsing and addition.
- **search_engine.py**: Tag-based search and result display.
- **order_system.py**: Order creation, modification, and submission.

### 5.4 Main Program (`main.py`)
- Provides a command-line interface.
- Integrates all functional modules.
- Generates SQL initialization script.

## 6. Test Data

The system includes the following test data:
- 2 vendors (V001, V002).
- 4 sample products (P1001-P1004).
- Complete test cases for the order processing flow.

## 7. Project Summary

This project implements the core functions of a multi-vendor e-commerce platform, featuring:
1. Well-normalized database design.
2. Modularized code structure.
3. Complete business logic implementation.
4. User-friendly command-line interface.

Future improvements include:
- Adding a user authentication system.
- Implementing more complex product search algorithms.
- Incorporating data analysis capabilities.