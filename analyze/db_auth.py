#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KSU Fucker
# -----------------
# Author:
#     Tasuku TAKAHASHI (supertask.jp)
# Coding style:
#     Google Python Style Guide
#     https://google.github.io/styleguide/pyguide.html
#
# I gave up the approch bellow because it doesn't work :(
#     https://qiita.com/Pampus/items/18b45330b990927652fd
#

import os
import boto3
import json
import mysql
import mysql.connector
from mysql.connector.constants import ClientFlag

auth_filename = "auth_info.txt"
AUTH_SAVED_PATH = '/Users/tasuku/.aws/' 
#AUTH_SAVED_PATH = '/'

class SQLAuth:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        auth_dict = json.load(open(AUTH_SAVED_PATH + auth_filename,'r'))
        region = auth_dict['db_region']
        user = auth_dict['db_user']
        password = auth_dict['db_password']
        host = auth_dict['db_host']
        port = auth_dict['db_port']
        rds = boto3.client('rds', region_name=region)
        #db_auth_token = rds.generate_db_auth_token(host, port, user, region)

        config = {
            'user': user,
            'password': password,
            'host': host,
            'db': 'imagenet',
            'client_flags': [ClientFlag.SSL],
            'ssl_ca': 'rds-combined-ca-bundle.pem'
        }
        return mysql.connector.connect(**config)

