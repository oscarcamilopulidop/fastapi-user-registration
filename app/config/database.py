from psycopg2 import pool


class Database:
    __connection_pool = None
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
            cls.__instance.__initialised = False
        return cls.__instance

    def initialise(self, **kwargs):
        if not self.__initialised:
            self.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)
            self.__initialised = True

    def get_connection(self):
        if self.__connection_pool:
            return self.__connection_pool.getconn()
        else:
            raise Exception("Connection pool is not initialized.")

    def return_connection(self, connection):
        self.__connection_pool.putconn(connection)

    def close_all_connections(self):
        self.__connection_pool.closeall()


class CursorFromConnectionPool:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database().get_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value:
            self.conn.rollback()
        else:
            self.cursor.close()
            self.conn.commit()
        Database().return_connection(self.conn)
