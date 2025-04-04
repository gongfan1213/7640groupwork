"""
Product Search Module
Implements tag-based product discovery functionality
"""
from db_conn import DBConnection

def search_by_tags(keyword, sort_order='asc'):
    """Search products by tag or name fragments
    Args:
        keyword (str): Search keyword for product name or tags
        sort_order (str): Sort order for price, 'asc' or 'desc'
    """
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
                ORDER BY p.price {}
            """.format('ASC' if sort_order == 'asc' else 'DESC')
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term, search_term))
            
            results = cursor.fetchall()
            if not results:
                print(f"\nNo products found related to '{keyword}'")
                return
                
            print(f"\nSearch results - Keyword: '{keyword}' (Sorted by price {'ascending' if sort_order == 'asc' else 'descending'})")
            print("{:<15} {:<30} {:<12} {:<25} {:<20}".format(
                'Product ID', 'Product Name', 'Price(HKD)', 'Tags', 'Vendor'))
            print("-" * 102)
            for product in results:
                print("{:<15} {:<30} ${:<11.2f} {:<25} {:<20}".format(
                    product['product_id'],
                    product['name'],
                    float(product['price']),
                    product['tags'],
                    product['vendor_name']))
    except Exception as e:
        print(f"Search error: {e}")
    finally:
        db.close()

# 测试代码
if __name__ == "__main__":
    search_by_tags("electronics")