import mysql.connector
from config import DatabaseConfig

db_conf = DatabaseConfig()


class Database:
    cnx_inside: bool = None

    def __init__(self) -> None:
        Database.cnx_inside = mysql.connector.connect(
            user=db_conf.user,
            password=db_conf.pw,
            host=db_conf.host,
            database=db_conf.db
        )
        print("Connected")

    @classmethod
    def connection(cls):
        print("get data")
        return Database.cnx_inside


class DBConnection:
    database: Database = None

    @staticmethod
    def get_connection() -> Database:
        if not DBConnection.database:
            DBConnection.database = Database()
        return DBConnection.database
