import sqlite3


def open_sql_cursor(sqlite_db_name):
    # Connect to DB and open cursor
    sql_conn = sqlite3.connect(sqlite_db_name)
    curr = sql_conn.cursor()
    return sql_conn, curr


def sql_bulk_insert(curr, table, data_set, col_list):
    ''' This function inserts'''
    col_string = ' (' + ', '.join(col_list) + ') '
    sql_query_string = 'insert or replace into ' + table + col_string + 'select '
    len_data_set = len(data_set)
    k = 0
    for data_row in data_set:
        len_data = len(data_row)
        curr_str = ''
        for i in range(0, len_data):
            curr_str += "'" + str(data_row[col_list[i]]) + "' as " + col_list[i]
            if i < len_data - 1:
                curr_str += ', '
        sql_query_string += curr_str
        if k < len_data_set - 1:
            sql_query_string += ' union select '
        k += 1
    sql_query_string += ';'
    ret_code = curr.execute(sql_query_string)
    ret_code = curr.execute("commit;")
    return ret_code


def close_conn(sql_conn):
    sql_conn.close()
    return

if __name__ == "__main__":
    from pdb import set_trace
    sql_conn, curr = open_sql_cursor('data/json.db')
    d1 = [{'a': 8,'b': 'data18', 'c':'test18'}, {'a': 19,'b': '1', 'c': 'test19'}, {'a': 100,'b': 'data100', 'c': 'test100'}]
    col_list = ['a', 'b', 'c']
    ret_code = sql_bulk_insert(curr, 'test', d1, col_list)