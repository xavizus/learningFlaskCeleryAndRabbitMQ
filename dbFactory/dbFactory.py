import importlib

class DatabaseFactory:
    # valid database types, with required info to function.
    VALIDDATABASETYPES = {
        "mysql": ('DB_TYPE', 'DB_DATABASE', 'DB_HOST', 'DB_USER', 'DB_PASS'),
        "mssql": None,
        "mariadb": None,
        "mongodb": None
    }

    # this function is called before the class is created.
    def __new__(cls, db):
        # Check if DB_TYPE is not in the validationtypes.
        if db['DB_TYPE'] not in cls.VALIDDATABASETYPES:
            raise Exception(f"Databasetype is invalid. Databasetype supplied: {db['DB_TYPE']}")

        # List for missing required config setitngs
        missing_required = []
        # Loop through all requried configs
        for require in cls.VALIDDATABASETYPES[db['DB_TYPE']]:
            # if not set.
            if not db.get(require):
                # add missing config to list.
                missing_required.append(require)

        # If list is not empty
        if missing_required:
            message = """There are some missing parameters in your
             config file. Missing following keys: """
             # add each key to the list
            for key in missing_required:
                message += f"{key}, "
            raise Exception(message)
        
        # Dynamically import module
        module = importlib.import_module("dbFactory.db"+db['DB_TYPE'])
        # Load the class
        class_ = getattr(module, 'DB'+db['DB_TYPE'])
        # Return the class initlized.
        return class_(db)
