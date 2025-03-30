"""Database connection module
Handles MySQL connection using PyMySQL
"""
import pymysql

class DBConnection:
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'root' 
        self.db = 'ecommerce'
        self.conn = None

    def connect(self):
        """Establish database connection"""
        try:
            # 检查MySQL服务是否可访问
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.host, 3307))
            if result != 0:
                print("错误: MySQL服务未启动或3307端口不可访问")
                return False
            
            # 尝试建立数据库连接
            self.conn = pymysql.connect(
                host=self.host,
                port=3307,
                user=self.user,
                password=self.password,
                db=self.db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            print("数据库连接成功建立")
            return True
            
        except pymysql.err.OperationalError as e:
            error_code = e.args[0]
            if error_code == 1045:
                print("错误: 用户名或密码不正确")
            elif error_code == 1044:
                print("错误: 用户权限不足")
            else:
                print(f"连接错误: {e}")
            return False
        except Exception as e:
            print(f"未知错误: {e}")
            return False

    def rollback(self):
        """Rollback current transaction"""
        if self.conn:
            self.conn.rollback()
            
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def get_cursor(self):
        """Get database cursor"""
        if not self.conn:
            if not self.connect():
                raise Exception("无法获取数据库游标：数据库连接失败")
        return self.conn.cursor()

    def commit(self):
        """Commit transaction"""
        self.conn.commit()