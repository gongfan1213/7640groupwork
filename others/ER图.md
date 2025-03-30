以下是根据你的数据库脚本和项目需求绘制的 **ER 图 (Entity-Relationship Diagram)** 设计，涵盖了所有主要实体及其关系。

---

### 📝 **ER 图结构说明**
#### ✅ 实体（Entities）
1. **vendors**: 供应商（Vendor ID, Name, Rating, Location）
2. **products**: 商品（Product ID, Name, Price, Tags, Vendor ID）
3. **customers**: 客户（Customer ID, Phone, Shipping Address）
4. **orders**: 订单（Order ID, Customer ID, Status, Created At）
5. **order_items**: 订单商品（Order ID, Product ID, Quantity）
6. **order_logs**: 订单日志（Log ID, Order ID, Action, Details, Log Time）

#### 🔗 关系（Relationships）
- vendors 和 products: 一对多 (1:N)，一个供应商可以有多个商品。
- customers 和 orders: 一对多 (1:N)，一个客户可以有多个订单。
- orders 和 order_items: 一对多 (1:N)，一个订单可以包含多个商品。
- orders 和 order_logs: 一对多 (1:N)，一个订单可以有多个日志记录。

---

### 📚 **ER 图设计**

1. **Vendor** (1) ➡️ (N) **Product**  
2. **Customer** (1) ➡️ (N) **Order**  
3. **Order** (1) ➡️ (N) **Order_Item**  
4. **Order** (1) ➡️ (N) **Order_Log**  

---

