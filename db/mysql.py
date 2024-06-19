import mysql.connector
from config.secret import secret

class mysql_connector:
    def __init__(self, config:secret) -> None:
        self.user_name = config.get("mysql", "user_name")
        self.passwd = config.get("mysql", "passwd")
        self.host_name = config.get("mysql", "host_name")
        self.db_name = config.get("mysql", "db_name")
        self.my_connect = None
        self.my_cursor = None
        self.connect()
        return
    
    def connect(self):
        try:
            self.my_connect = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                password=self.passwd,
                database=self.db_name
            )
            self.my_cursor = self.my_connect.cursor()
            return True
        except mysql.connector.Error as e:
            self.handle_db_error(e)
            self.close()
        return False
    
    def handle_db_error(self, e):
        error_code = getattr(e, 'errno', None)
        if error_code == mysql.connector.errorcode.CR_SERVER_LOST:
            print("MySQL server has gone away.")
        elif error_code == mysql.connector.errorcode.CR_SERVER_GONE_ERROR:
            print("MySQL server has gone away (CR_SERVER_GONE_ERROR).")
        else:
            print("MySQL Error: ", e)
    
    def close(self):
        if self.my_cursor is not None:
            self.my_cursor.close()
            self.my_cursor = None
            
        if self.my_connect is not None:
            self.my_connect.close()
            self.my_connect = None
    
    def read(self, sql:str):
        if self.my_cursor is None and not self.connect():
            return None, False
        
        try:
            self.my_cursor.execute(sql)
            result = self.my_cursor.fetchall()
            return result, True
        except mysql.connector.Error as e:
            self.handle_db_error(e)
            self.close()
        
        return None, False
        
    def write(self, sql:str):
        if self.my_cursor is None and not self.connect():
            return False
        
        try:
            self.my_cursor.execute(sql)
            self.my_connect.commit()
            return True
        except mysql.connector.Error as e:
            self.handle_db_error(e)
            self.close()
        
        return False