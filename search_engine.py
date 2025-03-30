"""
Product Search Module
Implements tag-based product discovery functionality
"""
from db_conn import DBConnection

def search_by_tags(keyword):
    """Search products by tag or name fragments"""
    db = DBConnection()
    try:
        db.connect()
        with db.get_cursor() as cursor:
            query = """
                SELECT p.product_id, p.name, p.price, p.tags, v.name as vendor_name
                FROM products p
                JOIN vendors v ON p.vendor_id = v.vendor_id
                WHERE p.tags LIKE %s
                   OR p.name LIKE %s
                ORDER BY p.price
            """
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term, search_term))
            
            results = cursor.fetchall()
            print(f"\nSearch Results for '{keyword}':")
            print("{:<15} {:<30} {:<10} {:<25} {:<20}".format(
                'Product ID', 'Name', 'Price', 'Tags', 'Vendor'))
            print("-" * 100)
            for product in results:
                print("{:<15} {:<30} HK${:<9} {:<25} {:<20}".format(
                    product['product_id'],
                    product['name'],
                    product['price'],
                    product['tags'],
                    product['vendor_name']))
    except Exception as e:
        print(f"Search error: {e}")
    finally:
        db.close()

# 测试代码
if __name__ == "__main__":
    search_by_tags("electronics")