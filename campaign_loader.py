#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Punchh Home Task
This command-line utility loads campaign data in JSON format into SQLite DB

'''
import os
from os.path import isdir, isfile
import sys
import glob
import argparse
import json
import logging
import hashlib
from datetime import datetime
from ConfigObject import ConfigObject

from config_processing import collect_property_file_contents
from sqlite_functions import *
##############################################
# Pre-checks for Python version and config
##############################################
if sys.version.title()[0] != '3':
    sys.exit('This program is developed for Python 3')


def b_string(string_value):
    ''' This function convert string to binary'''
    s = bytearray(string_value,"utf-8")
    b_str_value = int(hashlib.sha1(s).hexdigest(), 16) % (10 ** 8)
    return b_str_value

def main(file_name):

    # processing config.ini
    try:
        config_properties = collect_property_file_contents(f'./config/config.ini')
        DATA_DIR = config_properties['DATA_DIR']

        # Setting up system log file name
        LOG_FILE = config_properties['LOG_FILE']

        # Setting up system log file name
        sqlite_db_name = config_properties['SQLITE_DB']


        # Checking for System Log file name existence
        if os.path.isfile(LOG_FILE) != True:
            create_logfile_str = 'touch ' + LOG_FILE
            os.system(create_logfile_str)
        
        logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)

        # checking for existence of SQLiteDB
        ret_status = 0
        if os.path.isfile(sqlite_db_name) != True:
            msg = 'SQLite DB not found...exiting'
            print(msg)
            logging.error(msg)
            return -1

        # Load Json into list of dicts
        with open(file_name) as json_file:
            try:
                users_lst = []
                campaigns_lst = []
                stats_lst = []
                unsubscribed_lst = []
                json_data = json.load(json_file)

                for json_row in json_data:

                    curr_user_dict = {}
                    curr_campaign_dict = {}
                    curr_stats_dict = {}

                    # create a dict of users
                    if json_row['email_address']:
                        curr_user_dict['user_id'] = b_string(json_row['email_address'])
                        curr_user_dict['email_address'] = json_row['email_address']
                    if json_row['email_unsubscribed']:
                        curr_user_dict['email_unsubscribed'] = 1
                    else:
                        curr_user_dict['email_unsubscribed'] = 0
                    users_lst.append(curr_user_dict)

                    # create a dict of campaigns
                    if json_row['campaign_name']:
                        curr_campaign_dict['campaign_id'] = b_string(json_row['campaign_name'])
                        curr_campaign_dict['campaign_name'] = json_row['campaign_name']
                        campaigns_lst.append(curr_campaign_dict)
 
                    # create a dict of stats
                    curr_stats_dict['browser'] = json_row['browser']
                    if json_row['email_bounced'] == None:
                        curr_stats_dict['email_bounced'] = ''
                    else:
                        curr_stats_dict['email_bounced'] = json_row['email_bounced']

                    if json_row['email_opened'] == None:
                        curr_stats_dict['email_opened'] = ''
                    else:
                        curr_stats_dict['email_opened'] = json_row['email_opened']

                    if json_row['email_sent'] == None:
                        curr_stats_dict['email_sent'] = ''
                    else:
                        curr_stats_dict['email_sent'] = json_row['email_sent']

                    if json_row['email_unsubscribed'] == None:
                        curr_stats_dict['email_unsubscribed'] = ''
                    else:
                        curr_stats_dict['email_unsubscribed'] = json_row['email_unsubscribed']
                        unsubscribed_lst.append(json_row['email_address'])

                    if json_row['email_url_clicked'] == None:
                        curr_stats_dict['email_url_clicked'] = ''
                    else:
                        curr_stats_dict['email_url_clicked'] = json_row['email_url_clicked']

                    if json_row['user_subscribed'] == None:
                        curr_stats_dict['user_subscribed'] = ''
                    else:
                        curr_stats_dict['user_subscribed'] = json_row['user_subscribed']

                    curr_stats_dict['campaign_id'] = curr_campaign_dict['campaign_id']
                    curr_stats_dict['user_id'] = curr_user_dict['user_id']

                    stats_lst.append(curr_stats_dict)

                # Connect to SQLite DB
                sql_conn, curr = open_sql_cursor(sqlite_db_name)

                # Get columns
                col_user_col_list = get_columns(sql_conn, 'users')
                cmp_user_col_list = get_columns(sql_conn, 'campaigns')
                stats_col_list = get_columns(sql_conn, 'campaign_stats')

                # Insert user list into users table
                ret_usr_code = sql_dim_insert(curr, 'users', users_lst, col_user_col_list)
                ret_cmp_code = sql_dim_insert(curr, 'campaigns', campaigns_lst, cmp_user_col_list)
                ret_stat_code = sql_fact_insert(curr, 'campaign_stats', stats_lst, stats_col_list)
                if len(unsubscribed_lst) > 0:
                    unsub_code = sql_user_unsubscribe(curr, unsubscribed_lst, col_user_col_list)

            except Exception as e:
                msg = "Cannot process JSON data"
                logging.error(msg)
                ret_code = -1

    except Exception as e:
        msg = "Exception occurred while processing config.ini and log file info. Please check." + str(e)
        print(msg)
        return -1

    return


##############################################
#                   MAIN
##############################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="JSON ingestion utility into SQLite",\
        epilog="Example: python campaign_loader.py -c data/campaign_1.json")
    parser.add_argument("-c", "--campaignJSON", required=True, help="Enter JSON file name with campaign data")
    args = parser.parse_args()
    file_name =args.campaignJSON

    # file_name = sys.argv[1]
    if len(file_name) != 0:
        ret_code = main(file_name)
    else:
        print("ERROR: file name cannot be empty")
        ret_code = -1

    sys.exit(ret_code)
