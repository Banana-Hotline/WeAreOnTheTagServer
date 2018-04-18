import sqlite3
from sqlite3 import Error

def create_response(result, message):
    return {"data":{'Result':result,'Message':message}}
<<<<<<< HEAD

hit_notify_message_body = \
"""The number of hits has been updated in the database.
User %s has been struck %s times. 
User %s has %s tags
"""
=======

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
>>>>>>> 6207ff21bd3668a639655d4203188950cae00a2d
