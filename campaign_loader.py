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

    except Exception as e:
        msg = "Exception occurred while processing config.ini and log file info. Please check." + str(e)
        print(msg)
        return -1


    # load json file into structure

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

    if len(file_name.strip()) != 0:
        ret_code = main(file_name)
    else:
        print("ERROR: file name cannot be empty")
        ret_code = -1
    # Load Json into list of dicts
    with open(file_name) as json_file:
        try:
            users_lst = []
            campaigns_lst = []
            stats_lst = []
            json_data = json.load(json_file)

            from pdb import set_trace; set_trace()

            for json_row in json_data:

                curr_user_dict = {}
                curr_campaign_dict = {}
                curr_stats_dict = {}
                # create a dict of users
                if json_row['email_address']:
                    curr_user_dict['user_id'] = b_string(json_row['email_address'])
                    curr_user_dict['email_address'] = json_row['email_address']
                    if json_row['email_unsubscribed']:
                        curr_user_dict['email_unsubscribed'] = json_row['email_unsubscribed']
                    users_lst.append(curr_user_dict)

                # create a dict of campaigns
                if json_row['campaign_name']:
                    curr_campaign_dict['campaign_id'] = b_string(json_row['campaign_name'])
                    curr_campaign_dict['campaign_name'] = json_row['campaign_name']
                    campaigns_lst.append(curr_campaign_dict)
                # create a dict of stats
                curr_stats_dict['browser'] = json_row['browser']
                curr_stats_dict['email_bounced'] = json_row['email_bounced']
                curr_stats_dict['email_opened'] = json_row['email_opened']
                curr_stats_dict['email_sent'] = json_row['email_sent']
                curr_stats_dict['email_unsubscribed'] = json_row['email_unsubscribed']
                curr_stats_dict['email_url_clicked'] = json_row['email_url_clicked']
                curr_stats_dict['user_subscribed'] = json_row['user_subscribed']
                curr_stats_dict['campaign_id'] = curr_campaign_dict['campaign_id']
                curr_stats_dict['user_id'] = curr_user_dict['user_id']
                stats_lst.append(curr_stats_dict)
        except Exception as e:
            msg = "Cannot process JSON data"
            logging.error(msg)  
            ret_code = -1      

    sys.exit(ret_code)