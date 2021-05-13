import os, configparser
import json
import base64
import sqlite3
from shutil import copyfile
import requests, json
from bs4 import BeautifulSoup
import sqlite3
import gzip, os
import win32crypt
from Cryptodome.Cipher import AES

import setCookie

def getFromFile(str):
    config = configparser.ConfigParser()
    config.read('cookies.ini')
    return config['cookies'][str]

def getCSRFToken():
    # if selection == 1:
    try:
        return getFromFile('CSRFTOKEN')
    except:
        setCookie.setCookie()
        #
        # if not os.path.exists('cookies.ini'):
        #     print('Creating cookies config file..')
        #     config = configparser.ConfigParser()
        #     config['cookies'] = {}
        #     with open('cookies.ini', 'w') as file:
        #         config.write(file)

def getLeetcodeSession():
    # if selection == 1:
    try:
        return getFromFile('LEETCODE_SESSION')
    except:
        setCookie.setCookie()
        # if not os.path.exists('cookies.ini'):
        #     print('Creating cookies config file..')
        #     config = configparser.ConfigParser()
        #     config['cookies'] = {}
        #     with open('cookies.ini', 'w') as file:
        #         config.write(file)



