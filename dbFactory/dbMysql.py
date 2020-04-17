import DBFactory
import mysql.connector
from dbAbstract import DBFactory

class DatabaseMySQL(DBFactory):
    host = None

    database = None

    username = None

    password = None

    port = 3306

    db = None
    
    dbCursor = None

    def __init__(self, databaseInfo: dict):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        if port != None:
            self.port = port

    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            database = self.database,
            user=self.username,
            passwd=self.password,
            port=self.port
        )
        self.dbCursor = self.db.cursor()