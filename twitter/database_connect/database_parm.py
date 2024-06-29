
class Db_parm:
    def __init__(self):
        self.host = 'localhost'
        self.dbname = 'jimmy_database'
        self.password = 'home1234'
        self.user = 'jimmy'
        self.port = '5432'
    def __str__(self):
        return "database detail"