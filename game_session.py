# from sqlalchemy import create_engine
from server_utils import *
import sqlite3

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
    return create_response('Success',"joined session_id: %s" %session_id)

def create_session_db(db, session_id):
    conn = create_connection("session_%s.db" %session_id)
    sql_create_session_data_table = """ CREATE TABLE `SESSION_DATA` ( `session_id` INTEGER, `hit_player` INTEGER, `shooter_id` INTEGER, `hit_time` DATE );"""
    create_table(conn, sql_create_session_data_table)



def main():
    database = "laserdb.db"
    print "hello world"


    # create a database connection
    conn = create_connection(database)

    session_id = create_session(conn)

    # conn2 = create_connection("session_%s.db" %session_id)
    create_session_db("session_%s.db" %session_id, session_id)

    # print join_session(conn2, 1, session_id)
    print session_id


if __name__ == '__main__':
    main()
