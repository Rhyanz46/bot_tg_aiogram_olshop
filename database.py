import mysql.connector
from config import DatabaseConfig

db_conf = DatabaseConfig()


class Database:
    cnx_inside: bool = None

    def __init__(self) -> None:
        self.create_connection()

    @classmethod
    def create_connection(cls):
        print("connected")
        Database.cnx_inside = mysql.connector.connect(
            user=db_conf.user,
            password=db_conf.pw,
            host=db_conf.host,
            database=db_conf.db
        )

    def connection(self):
        if Database.cnx_inside.is_connected():
            return Database.cnx_inside
        else:
            print("reconnected")
            self.create_connection()
            return Database.cnx_inside


class DBConnection:
    database: Database = None

    @staticmethod
    def get_connection() -> Database:
        if not DBConnection.database:
            DBConnection.database = Database()
        return DBConnection.database
