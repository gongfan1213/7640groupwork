"""
Product Catalog Module
Handles product browsing and creation functions
"""
from db_conn import DBConnection
from models import Product

def browse_vendor_products(vendor_id):
    """Display all products from specific vendor"""
    db = DBConnection()
    try:
        db.connect()
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT product_id, name, price, tags 
                FROM products 
                WHERE vendor_id = %s
            """, (vendor_id,))
            
            products = cursor.fetchall()
            print(f"\nProducts from Vendor {vendor_id}:")
            print("{:<15} {:<30} {:<10} {:<30}".format(
                'Product ID', 'Name', 'Price', 'Tags'))
            print("-" * 85)
            for product in products:
                print("{:<15} {:<30} HK${:<9} {:<30}".format(
                    product['product_id'],
                    product['name'],
                    product['price'],
                    product['tags']))
    except Exception as e:
        print(f"Error fetching products: {e}")
    finally:
        db.close()

def add_new_product(vendor_id):
    """Create new product for specified vendor"""
    print("\nNew Product Creation:")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    price = float(input("Price: "))
    tags = [t.strip() for t in input("Tags (comma-separated): ").split(',')][:3]

    new_product = Product(product_id, name, price, tags, vendor_id)
    new_product.add_to_inventory()
    print("Product successfully added!")

# 测试代码
if __name__ == "__main__":
    vid = input("Enter Vendor ID: ").strip()
    browse_vendor_products(vid)
    add_new_product(vid)
    browse_vendor_products(vid)