import mysql.connector
from config import DatabaseConfig
from mysql.connector import errorcode

db_conf = DatabaseConfig()


def mysql_get_mydb():
    try:
        cnx_inside = mysql.connector.connect(
            user=db_conf.user,
            password=db_conf.pw,
            host=db_conf.host,
            database=db_conf.db
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        cnx_inside.close()
    return cnx_inside


cnx = mysql_get_mydb()
