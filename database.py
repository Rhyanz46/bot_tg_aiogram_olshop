import mysql.connector
from config import DatabaseConfig

db_conf = DatabaseConfig()
cnx = mysql.connector.connect(
    user=db_conf.user,
    password=db_conf.pw,
    host=db_conf.host,
    database=db_conf.db
)
