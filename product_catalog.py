"""
Product Catalog Module
Handles product browsing and creation functions
"""
from db_conn import DBConnection
from models import Product

def browse_vendor_products(vendor_id, page=1, per_page=10):
    """Display all products from specific vendor with pagination"""
    db = DBConnection()
    try:
        db.connect()
        with db.get_cursor() as cursor:
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM products WHERE vendor_id = %s", (vendor_id,))
            total = cursor.fetchone()['total']
            total_pages = (total + per_page - 1) // per_page
            
            # Get paginated results
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT product_id, name, price, tags 
                FROM products 
                WHERE vendor_id = %s
                LIMIT %s OFFSET %s
            """, (vendor_id, per_page, offset))
            
            products = cursor.fetchall()
            print(f"\nProducts from Vendor {vendor_id} (Page {page}/{total_pages}):")
            print("{:<15} {:<30} {:<10} {:<30}".format(
                'Product ID', 'Name', 'Price', 'Tags'))
            print("-" * 85)
            for product in products:
                print("{:<15} {:<30} HK${:<9} {:<30}".format(
                    product['product_id'],
                    product['name'],
                    product['price'],
                    product['tags']))
            
            if total_pages > 1:
                print(f"\nPage {page} of {total_pages} (Total products: {total})")
                if page < total_pages:
                    print("Enter 'n' for next page")
                if page > 1:
                    print("Enter 'p' for previous page")
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
    page = 1
    while True:
        browse_vendor_products(vid, page)
        cmd = input("\nEnter command (a: add product, n: next page, p: prev page, q: quit): ").strip().lower()
        if cmd == 'a':
            add_new_product(vid)
        elif cmd == 'n':
            page += 1
        elif cmd == 'p' and page > 1:
            page -= 1
        elif cmd == 'q':
            break