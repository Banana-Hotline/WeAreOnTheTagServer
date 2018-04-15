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
    sql = '''INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)'''
    cur = conn.cursor()
    cur.execute(sql)
    session_id = cur.lastrowid
    return create_respone('Success',"Created Session: %s" %session_id)

def main():
    database = "laserdb.db"
    print "hello world"


    # create a database connection
    conn = create_connection(database)

    print create_session(conn)
    # with conn:
    #     # create a new project
    #     project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    #     project_id = create_project(conn, project)
    #
    #     # tasks
    #     task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
    #     task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
    #
    #     # create tasks
    #     create_task(conn, task_1)
    #     create_task(conn, task_2)


if __name__ == '__main__':
    main()
