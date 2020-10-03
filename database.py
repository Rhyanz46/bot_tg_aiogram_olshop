import mysql.connector
from config import DatabaseConfig

db_conf = DatabaseConfig()


class Database:
    cnx_inside: bool = None

    def __init__(self) -> None:
        self.create_connection()

    @classmethod
    def create_connection(cls):
        Database.cnx_inside = mysql.connector.connect(
            user=db_conf.user,
            password=db_conf.pw,
            host=db_conf.host,
            database=db_conf.db
        )

    def connection(self):
        try:
            return Database.cnx_inside
        except:
            self.create_connection()
            return Database.cnx_inside



class DBConnection:
    database: Database = None

    @staticmethod
    def get_connection() -> Database:
        if not DBConnection.database:
            DBConnection.database = Database()
        return DBConnection.database
