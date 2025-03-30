"""
Database connection module
Handles MySQL connection using PyMySQL
"""
import pymysql

class DBConnection:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password'
        self.db = 'ecommerce'
        self.conn = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connection established")
        except pymysql.MySQLError as e:
            print(f"Connection error: {e}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def get_cursor(self):
        """Get database cursor"""
        return self.conn.cursor()

    def commit(self):
        """Commit transaction"""
        self.conn.commit()