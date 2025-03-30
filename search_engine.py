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
                print(f"\n未找到与 '{keyword}' 相关的产品")
                return
                
            print(f"\n搜索结果 - 关键词: '{keyword}' (按价格{'升序' if sort_order == 'asc' else '降序'})")
            print("{:<15} {:<30} {:<12} {:<25} {:<20}".format(
                '产品ID', '产品名称', '价格(HKD)', '标签', '供应商'))
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