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
    sql_create_session_data_table = """ CREATE TABLE `HIT_DATA` ( `session_id` INTEGER, `hit_player` INTEGER, `shooter_id` INTEGER, `hit_time` DATE );"""
    sql_create_accuracy_table = """ CREATE TABLE `SHOT_DATA` ( `session_id` INTEGER, `shooter_id` INTEGER, `times_fired` INTEGER );"""
    create_table(conn, sql_create_session_data_table)
    create_table(conn, sql_create_accuracy_table)

def add_hit_data(session_id, shooter_id, hit_player, shots_fired):
    conn = create_connection("session_%s.db" %session_id)
    print 'Inserting hit data'
    hit_sql = "insert into HIT_DATA (session_id,hit_player,shooter_id,hit_time) values (%s, %s, %s, datetime('now'));" %(session_id,hit_player,shooter_id)
    shot_sql = "insert into SHOT_DATA (session_id,shooter_id,times_fired) values (%s, %s, %s);" %(session_id,hit_player,shots_fired)
    conn.execute(hit_sql)
    conn.execute(shot_sql)

def main():
    database = "laserdb.db"
    print "hello world"


    # create a database connection
    conn = create_connection(database)

    session_id = create_session(conn)

    # conn2 = create_connection("session_%s.db" %session_id)
    create_session_db("session_%s.db" %session_id, session_id)
    add_hit_data(session_id,1,3,25)
    add_hit_data(session_id,1,2,4)
    add_hit_data(session_id,1,3,2)
    add_hit_data(session_id,3,2,56)
    add_hit_data(session_id,2,1,75)

    # print join_session(conn2, 1, session_id)
    print session_id


if __name__ == '__main__':
    main()
