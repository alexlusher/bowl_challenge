import sqlite3

def open_sql_cursor(sqlite_db_name):
    # Connect to DB and open cursor
    sql_conn = sqlite3.connect(sqlite_db_name)
    curr = sql_conn.cursor()
    return curr

def sql_bulk_insert(data_set):
    ret_code = 0
    return ret_code