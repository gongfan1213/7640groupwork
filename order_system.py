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
        if self.current_order is None:
            print("Please create an order first! Use option 1 to create a new order.")
            return
            
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
        if self.current_order is None:
            print("Please create an order first! Use option 1 to create a new order.")
            return

        if self.current_order.status != 'pending':
            print("Cannot modify shipped order")
            return

        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                # 验证商品是否在订单中
                found = False
                for item in self.current_order.items:
                    if item['product_id'] == product_id:
                        found = True
                        break
                
                if not found:
                    print(f"Product {product_id} not found in order")
                    return

                # 移除商品
                self.current_order.items = [item for item in self.current_order.items 
                                        if item['product_id'] != product_id]
                
                # 记录修改日志
                cursor.execute(
                    "INSERT INTO order_logs (order_id, action, details) VALUES (%s, %s, %s)",
                    (self.current_order.order_id, 'remove_item', f'Removed product {product_id}')
                )
                db.commit()
                print(f"Removed product {product_id} from order")

        except Exception as e:
            print(f"Error removing item: {e}")
            db.rollback()
        finally:
            db.close()

    def cancel_order(self):
        """Cancel order by order ID"""
        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                # 显示所有待处理订单
                cursor.execute(
                    "SELECT order_id, customer_id, status, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at FROM orders WHERE status = 'pending'"
                )
                orders = cursor.fetchall()
                if not orders:
                    print("No orders available for cancellation")
                    return
                
                print("\nPending Orders List:")
                print("Order ID\tCustomer ID\tCreation Time")
                for order in orders:
                    print(f"{order['order_id']}\t{order['customer_id']}\t{order['created_at']}")
                
                order_id = input("\nEnter order ID to cancel: ").strip()
                
                # 验证订单是否存在且状态为pending
                cursor.execute(
                    "SELECT status FROM orders WHERE order_id = %s",
                    (order_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    print("Order does not exist")
                    return
                    
                if order['status'] != 'pending':
                    print("Can only cancel pending orders")
                    return
                
                # 更新订单状态为已取消
                cursor.execute(
                    "UPDATE orders SET status = 'cancelled' WHERE order_id = %s",
                    (order_id,)
                )
                db.commit()
                print(f"Order {order_id} has been cancelled")
                
        except Exception as e:
            print(f"Error cancelling order: {e}")
            db.rollback()
        finally:
            db.close()

    def submit_order(self):
        """Finalize order and save to database"""
        if self.current_order is None:
            print("Please create an order first! Use option 1 to create a new order.")
            return

        if not self.current_order.items:
            print("No items in order! Please use option 2 to add items.")
            return
            
        if self.current_order.status != 'pending':
            print("Cannot submit order: Invalid order status")
            return

        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                # 验证库存并计算订单总额
                order_total = 0
                for item in self.current_order.items:
                    cursor.execute(
                        "SELECT price, stock FROM products WHERE product_id = %s",
                        (item['product_id'],)
                    )
                    product = cursor.fetchone()
                    if not product:
                        print(f"Product {item['product_id']} not found")
                        return
                    if product['stock'] < item['quantity']:
                        print(f"Insufficient stock for product {item['product_id']}")
                        return
                    order_total += product['price'] * item['quantity']

                # Save order header
                cursor.execute(
                    "INSERT INTO orders (order_id, customer_id, status, total_amount) VALUES (%s, %s, %s, %s)",
                    (self.current_order.order_id, 
                     self.current_order.customer_id,
                     'pending',
                     order_total)
                )

                # Save order items and update stock
                for item in self.current_order.items:
                    cursor.execute(
                        """INSERT INTO order_items 
                           (order_id, product_id, quantity) 
                           VALUES (%s, %s, %s)""",
                        (self.current_order.order_id,
                         item['product_id'],
                         item['quantity'])
                    )
                    # Update product stock
                    cursor.execute(
                        "UPDATE products SET stock = stock - %s WHERE product_id = %s",
                        (item['quantity'], item['product_id'])
                    )

                db.commit()
                self.current_order.status = 'submitted'
                print(f"Order successfully submitted! Total amount: HK${order_total:.2f}")

        except Exception as e:
            print(f"Error submitting order: {e}")
            db.conn.rollback()
        finally:
            db.close()

    def display_orders(self):
        """Display all orders with detailed information"""
        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT o.order_id, o.customer_id, o.status,
                           c.phone, c.shipping_address,
                           p.name as product_name, p.price,
                           oi.quantity,
                           (p.price * oi.quantity) as total_price
                    FROM orders o
                    LEFT JOIN customers c ON o.customer_id = c.customer_id
                    LEFT JOIN order_items oi ON o.order_id = oi.order_id
                    LEFT JOIN products p ON oi.product_id = p.product_id
                    ORDER BY o.order_id
                """)
                
                orders = cursor.fetchall()
                if not orders:
                    print("\nNo orders found")
                    return
                
                current_order_id = None
                order_total = 0
                
                for order in orders:
                    if current_order_id != order['order_id']:
                        if current_order_id is not None:
                            print(f"订单总金额: HK${order_total:.2f}\n")
                            print("-" * 80)
                        
                        current_order_id = order['order_id']
                        order_total = 0
                        
                        print(f"\n订单ID: {order['order_id']}")
                        print(f"客户ID: {order['customer_id']}")
                        print(f"联系电话: {order['phone']}")
                        print(f"配送地址: {order['shipping_address']}")
                        print(f"订单状态: {order['status']}")
                        print("\n商品明细:")
                        print("{:<30} {:<10} {:<10} {:<10}".format(
                            "商品名称", "单价", "数量", "小计"))
                        print("-" * 60)
                    
                    if order['product_name']:
                        line_total = order['total_price']
                        order_total += line_total
                        print("{:<30} HK${:<9.2f} {:<10} HK${:<9.2f}".format(
                            order['product_name'],
                            order['price'],
                            order['quantity'],
                            line_total))
                
                if orders:
                    print(f"订单总金额: HK${order_total:.2f}\n")
                    print("-" * 80)
                
        except Exception as e:
            print(f"查询订单时发生错误: {e}")
        finally:
            db.close()

# 测试代码
if __name__ == "__main__":
    system = OrderSystem()
    system.display_orders()
    system.create_order("CUST001")
    system.add_item("P123", 2)
    system.submit_order()