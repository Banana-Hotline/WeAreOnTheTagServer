# from sqlalchemy import create_engine
import server_utils
import sqlite3

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

def create_session(conn):
    sql = '''insert into GAME_SESSION (start_time,state) values (datetime('now'), 'WAITING')'''
    cur = conn.cursor()
    cur.execute(sql)
    session_id = cur.lastrowid
    return session_id

def join_session(conn, user_id, session_id):
    sql = 'update GAME_SESSION set player_1=\''+ str(user_id) + '\' where session_id =\'' + str(session_id) + '\''
    cur = conn.cursor()
    cur.execute(sql)
    session_id = cur.lastrowid
    return server_utils.create_respone('Success',"joined session_id: %s" %session_id)



def main():
    database = "laserdb.db"
    print "hello world"


    # create a database connection
    conn = create_connection(database)

    session_id = create_session(conn)
    join_session(conn, 1, session_id)
    print session_id


if __name__ == '__main__':
    main()
