import csv
from faker import Faker
import uuid

fake = Faker('zh_CN')

def generate_vendors(num=10):
    vendors = []
    for _ in range(num):
        vendors.append({
            'vendor_id': str(uuid.uuid4()),
            'name': fake.company(),
            'rating': round(fake.pyfloat(min_value=1.0, max_value=5.0, right_digits=1), 1),
            'location': fake.province() + '-' + fake.city()
        })
    return vendors

def generate_products(vendors, products_per_vendor=5):
    products = []
    tags_pool = ['数码', '服装', '家居', '美妆', '食品', '运动', '图书', '母婴', '汽车', '电器']
    
    for vendor in vendors:
        for _ in range(products_per_vendor):
            products.append({
                'product_id': str(uuid.uuid4()),
                'vendor_id': vendor['vendor_id'],
                'name': fake.word().join(fake.words(2)),
                'price': round(fake.pyfloat(min_value=10, max_value=1000, right_digits=2), 2),
                'tags': ','.join(fake.random_elements(elements=tags_pool, length=3, unique=True)),
                'stock': fake.random_int(min=0, max=1000)
            })
    return products

def generate_customers(num=50):
    customers = []
    for _ in range(num):
        customers.append({
            'customer_id': str(uuid.uuid4()),
            'phone': fake.phone_number(),
            'address': fake.address()
        })
    return customers

def generate_sql(vendors, products, customers):
    sql = []
    sql.append('START TRANSACTION;\n')
    
    # Insert vendors
    sql.append('INSERT INTO vendors (vendor_id, name, rating, location) VALUES\n')
    vendor_values = [
        "('{}', '{}', {}, '{}')".format(v['vendor_id'], v['name'], v['rating'], v['location']) 
        for v in vendors
    ]
    sql.append(',\n'.join(vendor_values) + ';\n')

    # Insert products
    sql.append('\nINSERT INTO products (product_id, vendor_id, name, price, tags, stock) VALUES\n')
    product_values = [
        "('{}', '{}', '{}', {}, '{}', {})".format(p['product_id'], p['vendor_id'], p['name'], p['price'], p['tags'], p['stock']) 
        for p in products
    ]
    sql.append(',\n'.join(product_values) + ';\n')

    # Insert customers
    sql.append('\nINSERT INTO customers (customer_id, phone, address) VALUES\n')
    customer_values = [
        "('{}', '{}', '{}')".format(c['customer_id'], c['phone'], c['address']) 
        for c in customers
    ]
    sql.append(',\n'.join(customer_values) + ';\n')

    sql.append('\nCOMMIT;')
    return '\n'.join(sql)

if __name__ == '__main__':
    vendors = generate_vendors(20)
    products = generate_products(vendors)
    customers = generate_customers(100)
    
    sql_content = generate_sql(vendors, products, customers)
    
    with open('groupX_insert_sql.txt', 'a', encoding='utf-8') as f:
        f.write('\n\n-- 自动生成的测试数据\n')
        f.write(sql_content)