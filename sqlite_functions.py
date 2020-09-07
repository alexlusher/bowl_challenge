from datetime import datetime
import sqlite3


def open_sql_cursor(sqlite_db_name):
    # Connect to DB and open cursor
    sql_conn = sqlite3.connect(sqlite_db_name)
    curr = sql_conn.cursor()
    return sql_conn, curr


def get_columns(sql_conn, table_name):
    ''' Retrieve list of table columns '''
    query_p1 = 'select * from '
    query_p2 = ' where 1=2;'
    query_string = query_p1 + table_name + query_p2
    cursor = sql_conn.execute(query_string)
    col_list = list(map(lambda x: x[0], cursor.description))
    return col_list


def sql_dim_insert(curr, table, data_set, col_list):
    ''' This function inserts multiple rows into users and campaigns tables'''
    dtr = datetime.now()
    stmp = dtr.strftime("%Y-%b-%d %H:%M:%S")

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
        curr_str += ', ' + "'" + stmp + "'" + ' as updated'    
        sql_query_string += curr_str
        condition = ' where not exists(select 1 from ' + table + ' where ' + col_list[0] + '=' + str(data_row[col_list[0]]) + ' limit 1)'
        sql_query_string += condition
        if k < len_data_set - 1:
            sql_query_string += ' union select '
        k += 1
    sql_query_string += ';'
    sql_code = curr.execute(sql_query_string)
    ret_code = curr.execute("commit;")
    return ret_code


def sql_fact_insert(curr, table, data_set, col_list):
    ''' This function inserts multiple rows into campaign_stats'''
    dtr = datetime.now()
    stmp = dtr.strftime("%Y-%b-%d %H:%M:%S")

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
        curr_str += ', ' + "'" + stmp + "'" + ' as updated'    
        sql_query_string += curr_str
        condition = ' where not exists(select 1 from ' + table + ' where ' + col_list[0] + '=' + str(data_row[col_list[0]]) + ' and ' + col_list[1] + '=' + str(data_row[col_list[1]]) + ' limit 1)'
        sql_query_string += condition
        if k < len_data_set - 1:
            sql_query_string += ' union select '
        k += 1
    sql_query_string += ';'
    sql_code = curr.execute(sql_query_string)
    ret_code = curr.execute("commit;")
    return ret_code


def sql_user_unsubscribe(curr, unsubscribed_lst, col_user_col_list):
    for unsub_rec in unsubscribed_lst:
        sql_query_string = 'update users set email_unsubscribed = 1 where email_address = ' + "'" + unsub_rec + "';"
        sql_code = curr.execute(sql_query_string)
    ret_code = curr.execute("commit;")
    return ret_code


def close_conn(sql_conn):
    sql_conn.close()
    return
