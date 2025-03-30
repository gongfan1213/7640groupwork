"""
Order System Module
Handles order creation, modification and status management
"""
from db_conn import DBConnection
from models import Order

class OrderSystem:
    """Manages order lifecycle including modifications"""
    def __init__(self):
        self.current_order = None

    def create_order(self, customer_id):
        """Initialize new order with unique ID"""
        order_id = input("Enter Order ID: ").strip()
        self.current_order = Order(order_id, customer_id)
        print(f"New order {order_id} created")

    def add_item(self, product_id, quantity):
        """Add product to current order"""
        if self.current_order.status != 'pending':
            print("Cannot modify shipped order")
            return

        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                # Verify product existence
                cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                if not cursor.fetchone():
                    print("Invalid product ID")
                    return

                # Add to order items
                self.current_order.items.append({
                    'product_id': product_id,
                    'quantity': quantity
                })
                print(f"Added {quantity}x {product_id} to order")

        except Exception as e:
            print(f"Error adding item: {e}")
        finally:
            db.close()

    def remove_item(self, product_id):
        """Remove product from current order"""
        if self.current_order.status != 'pending':
            print("Cannot modify shipped order")
            return

        self.current_order.items = [item for item in self.current_order.items 
                                   if item['product_id'] != product_id]
        print(f"Removed {product_id} from order")

    def cancel_order(self):
        """Cancel current order before shipping"""
        if self.current_order.status != 'pending':
            print("Cannot cancel shipped order")
            return

        self.current_order.status = 'cancelled'
        print("Order cancelled")

    def submit_order(self):
        """Finalize order and save to database"""
        if not self.current_order.items:
            print("Cannot submit empty order")
            return

        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                # Save order header
                cursor.execute(
                    "INSERT INTO orders (order_id, customer_id, status) VALUES (%s, %s, %s)",
                    (self.current_order.order_id, 
                     self.current_order.customer_id,
                     'pending')
                )

                # Save order items
                for item in self.current_order.items:
                    cursor.execute(
                        """INSERT INTO order_items 
                           (order_id, product_id, quantity) 
                           VALUES (%s, %s, %s)""",
                        (self.current_order.order_id,
                         item['product_id'],
                         item['quantity'])
                    )

                db.commit()
                print("Order successfully submitted!")

        except Exception as e:
            print(f"Error submitting order: {e}")
            db.conn.rollback()
        finally:
            db.close()

# 测试代码
if __name__ == "__main__":
    system = OrderSystem()
    system.create_order("CUST001")
    system.add_item("P123", 2)
    system.submit_order()