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
import logging
from datetime import datetime
from ConfigObject import ConfigObject

from config_processing import collect_property_file_contents
from sqlite_functions import *
##############################################
# Pre-checks for Python version and config
##############################################
if sys.version.title()[0] != '3':
    sys.exit('This program is developed for Python 3')


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
        
        logger = logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)

        # checking for existence of SQLiteDB
        ret_status = 0
        if os.path.isfile(sqlite_db_name) != True:
            msg = 'SQLite DB not found...exiting'
            print(msg)
            logger.error(msg)
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

    sys.exit(ret_code)