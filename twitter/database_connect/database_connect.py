import psycopg2
import psycopg2.extras
from database_connect.database_parm import Db_parm

class Db_connect(Db_parm):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cur = None
        try:
            self.conn = psycopg2.connect(dbname=self.dbname,
                                         host=self.host,
                                         port=self.port,
                                         user=self.user,
                                         password=self.password)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.Error as e:
            print(e)
            print('database 連接失敗')
    
    def db_fetchall(self,stmt,data=None):
        try:
            self.cur.execute(stmt,data)
            rows = self.cur.fetchall()
        except:
            rows = list()
        return rows
    
    def db_fetchone(self,stmt,data=None):
        try:
            self.cur.execute(stmt,data)
            rows = self.cur.fetchone()
        except:
            rows = list()
        return rows
    
    def db_execute(self,stmt,data=None):
        try:
            self.cur.execute(stmt,data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Failed to execute statement: {e}")
    
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    
    def __str__(self):
        return "database的操作"                