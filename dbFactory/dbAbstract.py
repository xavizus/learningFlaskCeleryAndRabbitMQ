from abc import ABC, abstractmethod
class Abstract_Database():

    @property
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def database(self):
        pass

    @property
    @abstractmethod
    def username(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def port(self):
        pass

    @abstractmethod
    def __init__(self, host, database, username, password, port = None):
        pass

    @abstractmethod
    def connect(self):
        pass
