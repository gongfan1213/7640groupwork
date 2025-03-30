"""
Vendor Management Module
Handles vendor listing and onboarding functions
"""
from db_conn import DBConnection
from models import Vendor

def display_vendors():
    """Display all vendors in formatted table"""
    db = DBConnection()
    try:
        db.connect()
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM vendors")
            vendors = cursor.fetchall()
            
            print("\n{:<15} {:<20} {:<8} {:<15}".format(
                'Vendor ID', 'Name', 'Rating', 'Location'))
            print("-" * 60)
            for vendor in vendors:
                print("{:<15} {:<20} {:<8} {:<15}".format(
                    vendor['vendor_id'],
                    vendor['name'],
                    vendor['rating'],
                    vendor['location']))
    except Exception as e:
        print(f"Error fetching vendors: {e}")
    finally:
        db.close()

def add_new_vendor():
    """Collect vendor data and create new vendor"""
    print("\nNew Vendor Registration:")
    vendor_id = input("Vendor ID: ").strip()
    name = input("Business Name: ").strip()
    rating = float(input("Initial Rating (0-5): "))
    location = input("Location: ").strip()

    new_vendor = Vendor(vendor_id, name, rating, location)
    new_vendor.save_to_db()
    print("Vendor successfully registered!")

# 测试代码
if __name__ == "__main__":
    display_vendors()
    add_new_vendor()
    display_vendors()