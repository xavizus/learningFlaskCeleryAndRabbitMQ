
class databaseFactory:
    databaseType = None

    databaseName = None

    serverAddress = None

    serverPort = None

    username = None

    password = None

    VALIDDATABASETYPES = {
        "mysql",
        "mssql",
        "mariadb",
        "mongodb"
    }

    def __init__(self, db):
        self.initilize(dburi)
        print(f"Database Type: {self.databaseType}")
        pass

    def initilize(self, uri):
        uri = uri.split(":",2)
        if uri[0].lower() not in self.VALIDDATABASETYPES:
            raise Exception(f"Databasetype is invalid. Databasetype supplied: {uri[0]}")
        self.databaseType = uri[0]

