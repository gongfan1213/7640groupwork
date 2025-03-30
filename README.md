# COMP7640 数据库系统与管理 - 在线零售平台

## 项目概述
本系统实现了一个多供应商电商平台，包含供应商管理、产品目录、订单系统和智能搜索功能。系统采用Python 3.5开发，使用PyMySQL连接MySQL数据库，通过数据库连接池管理并发访问。

## 系统架构
```
├── db_conn.py        # 数据库连接池管理
├── models.py         # 数据模型定义（供应商/产品/客户/订单）
├── vendor_mgmt.py    # 供应商管理系统
├── product_catalog.py # 产品目录管理
├── order_system.py   # 订单生命周期管理
├── search_engine.py   # 标签驱动搜索系统
├── main.py           # 命令行菜单入口
└── groupX_insert_sql.txt # 数据库初始化脚本
```

## 安装与运行
```bash
# 安装依赖
pip install PyMySQL==0.9.3

# 初始化数据库
mysql -u root -p < groupX_insert_sql.txt

# 启动系统
python main.py
```

## 核心模块解析

### 1. 数据库连接池 (db_conn.py)
```python
class DBConnection:
    """数据库连接池管理（单例模式）
    功能特性：
    - 线程安全的连接池初始化
    - 支持with语句自动归还连接
    - 连接健康检查机制
    典型用法：
    db = DBConnection()
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM vendors')
    """
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.pool = QueuePool(
                creator=connect,
                max_overflow=10,
                timeout=300
            )
        return cls._instance
```

### 2. 数据模型 (models.py)
```python
class Vendor:
    """供应商模型
    属性：vendor_id, name, rating, location
    方法：save_to_db() 持久化到数据库"""

class Product:
    """产品模型
    属性：product_id, name, price, tags(最多3个)
    方法：add_to_inventory() 加入供应商库存"""
```

### 3. 供应商管理系统 (vendor_mgmt.py)
```python
def register_vendor():
    """供应商注册流程
    1. 生成UUID格式的vendor_id
    2. 验证评分范围(1.0-5.0)
    3. 地理位置格式校验（省份-城市）
    4. 自动生成初始化产品目录"""
    
    # 示例代码片段
    while True:
        rating = float(input('请输入评分(1.0-5.0): '))
        if 1.0 <= rating <= 5.0:
            break
    # 生成唯一ID
    vendor_id = str(uuid.uuid4())
    
class VendorAPI:
    """RESTful 接口设计
    GET /api/vendors → 获取供应商列表
    POST /api/vendors → 创建新供应商
    PUT /api/vendors/{id} → 更新供应商信息"""
```

### 4. 订单系统 (order_system.py)
```python
class Order:
    """订单生命周期管理
    - create_order(): 创建新订单
    - add_item(): 添加商品（支持跨供应商）
    - cancel_order(): 取消未发货订单
    - generate_receipt(): 生成交易凭证"""
```

## SQL脚本使用指南
### 自动生成机制
```python
def generate_sql_script():
    """自动生成groupX_insert_sql.txt
    包含：
    1. 动态生成测试数据
    2. 事务批处理优化
    3. 外键约束处理"""
    
    # 示例生成逻辑
    with open('groupX_insert_sql.txt', 'w') as f:
        f.write('CREATE TABLE IF NOT EXISTS products (\n')
        f.write('    product_id VARCHAR(36) PRIMARY KEY,\n')
        
### 使用示例
```bash
# 生成增量更新脚本（每天03:00自动执行）
mysqldump -u root -p --no-create-info retail_platform > update_$(date +%F).sql

# 执行事务性更新
mysql -u root -p -e "
START TRANSACTION;
SOURCE groupX_insert_sql.txt; 
COMMIT;"
```

2. 使用方式：
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS retail_platform;

-- 创建供应商表
CREATE TABLE vendors (
    vendor_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rating DECIMAL(2,1) CHECK (rating BETWEEN 1 AND 5),
    location VARCHAR(50)
);
```

3. 数据维护：
- 每日自动备份：`mysqldump -u root -p retail_platform > backup.sql`
- 快速恢复：`mysql -u root -p retail_platform < backup.sql`

## 故障排除
- 连接池耗尽：检查数据库最大连接数设置
- 标签搜索失效：确保产品tags字段使用逗号分隔
- 订单状态异常：验证事务隔离级别（默认REPEATABLE READ）