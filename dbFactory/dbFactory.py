import importlib

class DatabaseFactory:
    VALIDDATABASETYPES = {
        "mysql": ('DB_TYPE', 'DB_DATABASE', 'DB_HOST', 'DB_USER', 'DB_PASS'),
        "mssql": None,
        "mariadb": None,
        "mongodb": None
    }

    def __new__(cls, db):
        if db['DB_TYPE'] not in cls.VALIDDATABASETYPES:
            raise Exception(f"Databasetype is invalid. Databasetype supplied: {db['DB_TYPE']}")

        missing_required = []
        for require in cls.VALIDDATABASETYPES[db['DB_TYPE']]:
            if not db.get(require):
                missing_required.append(require)
        if missing_required:
            message = """There are some missing parameters in your
             config file. Missing following keys: """
            for key in missing_required:
                message += f"{key}, "
            raise Exception(message)

        module = importlib.import_module("dbFactory.db"+db['DB_TYPE'])
        class_ = getattr(module, 'DB'+db['DB_TYPE'])
        return class_(db)
