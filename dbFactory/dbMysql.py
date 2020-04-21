import mysql.connector
from dbFactory.dbAbstract import DBFactory

class DBmysql(DBFactory):
    host = None

    database = None

    username = None

    password = None

    port = 3306

    db = None

    db_cursor = None

    def __init__(self, databaseInfo: dict):
        self.host = databaseInfo['DB_HOST']
        self.username = databaseInfo['DB_USER']
        self.password = databaseInfo['DB_PASS']
        self.database = databaseInfo['DB_DATABASE']
        if databaseInfo['DB_PORT'] is not None:
            self.port = databaseInfo['DB_PORT']

    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            database = self.database,
            user=self.username,
            passwd=self.password,
            port=self.port
        )
        self.db_cursor = self.db.cursor()

    def commit(self):
        self.db.commit()

    def execute(self, sql, values = None):
        self.db_cursor.execute(sql, values)

    def rowcount(self):
        return self.db_cursor.rowcount
    