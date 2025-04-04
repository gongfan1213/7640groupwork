"""
Data models module
Defines core business entities and database operations
"""
from db_conn import DBConnection

class Vendor:
    """Represents e-commerce platform vendor"""
    def __init__(self, vendor_id, name, rating, location):
        self.vendor_id = vendor_id
        self.name = name
        self.rating = rating
        self.location = location
        self.products = []

    def save_to_db(self):
        """Save vendor to database"""
        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                sql = """INSERT INTO vendors 
                       (vendor_id, name, rating, location) 
                       VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (self.vendor_id, self.name, 
                                   self.rating, self.location))
                db.commit()
        except Exception as e:
            print(f"Error saving vendor: {e}")
        finally:
            db.close()

class Product:
    """Represents product entity with tag system"""
    def __init__(self, product_id, name, price, tags, vendor_id):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.tags = tags[:3]  # Enforce max 3 tags
        self.vendor_id = vendor_id

    def add_to_inventory(self):
        """Add product to vendor's inventory"""
        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                sql = """INSERT INTO products 
                       (product_id, name, price, tags, vendor_id) 
                       VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (self.product_id, self.name,
                                   self.price, ",".join(self.tags),
                                   self.vendor_id))
                db.commit()
        except Exception as e:
            print(f"Error adding product: {e}")
        finally:
            db.close()

# 类似地实现Customer和Order类
class Customer:
    """Represents customer profile"""
    def __init__(self, customer_id, phone, shipping_address):
        self.customer_id = customer_id
        self.phone = phone
        self.shipping_address = shipping_address

# models.py
class Order:
    """订单对象，包含完整订单信息"""
    def __init__(self, order_id, customer_id, status, created_at, items=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.status = status
        self.items = items if items is not None else []
        self.created_at = created_at