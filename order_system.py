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

    def select_order(self):
        """Select existing order from database"""
        db = DBConnection()
        try:
            db.connect()
            with db.get_cursor() as cursor:
                cursor.execute("SELECT order_id, customer_id, status FROM orders WHERE status = 'pending'")
                orders = cursor.fetchall()
                if not orders:
                    print("No pending orders available")
                    return False
                    
                print("\nAvailable Orders:")
                for idx, order in enumerate(orders, 1):
                    print(f"{idx}. Order ID: {order['order_id']}, Customer: {order['customer_id']}")
                
                choice = input("\nSelect order number (or 0 to create new): ").strip()
                if choice == '0':
                    customer_id = input("Enter Customer ID: ").strip()
                    import uuid
                    while True:
                        order_id = str(uuid.uuid4())  # Generate full UUID as order ID
                        cursor.execute("SELECT 1 FROM orders WHERE order_id = %s", (order_id,))
                        if not cursor.fetchone():  # Check if ID exists
                            break
                    self.current_order = Order(order_id, customer_id)
                    print(f"New order {order_id} created")
                    return True
                
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(orders):
                        selected = orders[choice_idx]
                        self.current_order = Order(
                            order_id=selected['order_id'],
                            customer_id=selected['customer_id'],
                            status=selected['status']  # 通过构造函数设置状态
                        )
                        
                        # Load order items
                        cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id = %s", 
                                      (selected['order_id'],))
                        self.current_order.items = [{'product_id': row['product_id'], 'quantity': row['quantity']} 
                                                  for row in cursor.fetchall()]
                        print(f"Selected order {selected['order_id']}")
                        return True
                except ValueError:
                    pass
                
                print("Invalid selection")
                return False
        except Exception as e:
            print(f"Error selecting order: {e}")
            return False
        finally:
            db.close()

    def add_item(self, product_id, quantity):
        """Add product to current order"""
        if self.current_order is None:
            print("Please select or create an order first!")
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
            print("Please select or create an order first!")
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
                # 临时注释掉order_logs表操作
                # cursor.execute(
                #     "INSERT INTO order_logs (order_id, action, details) VALUES (%s, %s, %s)",
                #     (self.current_order.order_id, 'remove_item', f'Removed product {product_id}')
                # )
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
                    "SELECT order_id, customer_id, status FROM orders WHERE status = 'pending'"
                )
                orders = cursor.fetchall()
                if not orders:
                    print("No orders available for cancellation")
                    return
                
                print("\nPending Orders List:")
                print("Order ID\tCustomer ID\tCreation Time")
                for order in orders:
                    print(f"{order['order_id']}\t{order['customer_id']}")
                
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
            print("Please select or create an order first!")
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
                # 计算订单总额
                order_total = 0
                for item in self.current_order.items:
                    cursor.execute(
                        "SELECT price FROM products WHERE product_id = %s",
                        (item['product_id'],)
                    )
                    product = cursor.fetchone()
                    if not product:
                        print(f"Product {item['product_id']} not found")
                        return
                    order_total += product['price'] * item['quantity']

                # 更新订单状态
                cursor.execute(
                    "UPDATE orders SET status = 'shipped' WHERE order_id = %s",
                    (self.current_order.order_id,)
                )

                # 删除已有的订单项
                cursor.execute(
                    "DELETE FROM order_items WHERE order_id = %s",
                    (self.current_order.order_id,)
                )

                # 保存订单项
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
                self.current_order.status = 'shipped'
                print(f"订单提交成功！总金额: HK${order_total:.2f}")

        except Exception as e:
            print(f"订单提交失败: {str(e)}")
            db.rollback()
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

    def create_order(self):
        """创建新订单并录入商品信息"""
        customer_id = input("请输入客户ID: ").strip()
        db = DBConnection()
        try:
            if not db.connect():
                return False

            with db.get_cursor() as cursor:
                # 验证客户有效性
                cursor.execute(
                    "SELECT customer_id FROM customers WHERE customer_id = %s",
                    (customer_id,)
                )
                db.commit()
                if not cursor.fetchone():
                    print(f"\033[31m错误：客户 {customer_id} 不存在\033[0m")
                    return False


                # 获取唯一订单ID
                while True:
                    order_id = input("请输入订单ID（20字符以内）: ").strip()
                    if not order_id:
                        print("\033[31m错误：订单ID不能为空\033[0m")
                        continue
                    if len(order_id) > 20:
                        print("\033[31m错误：订单ID超过20字符限制\033[0m")
                        continue

                    cursor.execute("SELECT 1 FROM orders WHERE order_id = %s", (order_id,))
                    if cursor.fetchone():
                        print("\033[31m错误：该订单ID已存在\033[0m")
                    else:
                        break
                    db.commit()
                # 输入订单状态
                valid_status = {'pending', 'shipped', 'cancelled'}
                while True:
                    status = input("请输入订单状态（pending/shipped/cancelled）: ").strip().lower()
                    if status in valid_status:
                        break
                    print("\033[31m错误：无效状态，请重新输入\033[0m")

                # 创建订单记录
                cursor.execute(
                    """INSERT INTO orders 
                       (order_id, customer_id, status, created_at) 
                       VALUES (%s, %s, %s, NOW())""",
                    (order_id, customer_id, status)
                )
                db.commit()

                # 录入商品信息
                items = []
                print("\n\033[33m开始录入商品（直接回车结束）\033[0m")
                while True:
                    product_id = input("\n输入Product_id: ").strip()
                    if not product_id:
                        print("\033[33m结束商品录入\033[0m")
                        break

                    # 验证商品有效性
                    cursor.execute(
                        "SELECT product_id, price FROM products WHERE product_id = %s",
                        (product_id,)
                    )
                    db.commit()
                    product = cursor.fetchone()
                    if not product:
                        print(f"\033[31m错误：商品 {product_id} 不存在\033[0m")
                        continue

                    # 输入购买数量
                    while True:
                        quantity = input("请输入购买数量: ").strip()
                        try:
                            quantity = int(quantity)
                            if quantity <= 0:
                                raise ValueError
                            break
                        except ValueError:
                            print("\033[31m错误：请输入有效正整数\033[0m")

                    # 添加订单商品
                    cursor.execute(
                        """INSERT INTO order_items 
                           (order_id, product_id, quantity) 
                           VALUES (%s, %s, %s)""",
                        (order_id, product_id, quantity)
                    )
                    db.commit()
                    items.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'price': product['price']
                    })
                    print(f"\033[32m已添加 {product_id} x{quantity}\033[0m")

                # 获取数据库生成的创建时间
                cursor.execute(
                    "SELECT created_at FROM orders WHERE order_id = %s",
                    (order_id,)
                )
                created_at = cursor.fetchone()['created_at']
                db.commit()

                # 初始化订单对象
                self.current_order = Order(
                    order_id=order_id,
                    customer_id=customer_id,
                    status=status,
                    created_at=created_at,
                    items=items
                )

            db.commit()
            print(f"\n\033[32m订单创建成功！\033[0m")
            print(f"订单号：{order_id}")
            print(f"创建时间：{self.current_order.created_at}")
            return True

        except Exception as e:
            print(f"\033[31m订单创建失败: {str(e)}\033[0m")
            db.rollback()
            return False

        finally:
            db.close()


# 测试代码
if __name__ == "__main__":
    system = OrderSystem()
    system.display_orders()
    system.create_order()
    system.add_item("P123", 2)
    system.submit_order()