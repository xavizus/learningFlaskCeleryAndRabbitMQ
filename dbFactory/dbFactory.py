
class databaseFactory:
    databaseType = None

    databaseName = None

    serverAddress = None

    serverPort = None

    username = None

    password = None

    required = (
        'DB_TYPE'
        'DB_DATABASE',
        'DB_HOST',
        'DB_PORT',
        'DB_USER',
        'DB_PASS'
    )

    VALIDDATABASETYPES = {
        "mysql",
        "mssql",
        "mariadb",
        "mongodb"
    }

    def __init__(self, db):
        self.initilize(db)
        print(f"Database Type: {self.databaseType}")
        pass

    def initilize(self, db):
        if db['DB_TYPE'] not in self.VALIDDATABASETYPES:
            raise Exception(f"Databasetype is invalid. Databasetype supplied: {db['DB_TYPE']}")

        missingRequired = []
        for require in self.required:
            if db[require] is None:
                missingRequired.append(require)
        
        if missingRequired:
            message = "There are some missing parameters in your config file. Missing following keys: "
            for missing in missingRequired:
                message += f"{missing}, "
            raise Exception(message)

        self.databaseType = db['DB_TYPE']
        self.databaseName = db['DB_DATABASE']
        self.serverAddress = db['DB_HOST']
        self.serverPort = db['DB_PORT']
        self.username = db['DB_USER']
        self.password = db['DB_PASS']
        