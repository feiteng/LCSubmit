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

encrypted_key = None
with open(os.getenv("APPDATA") + "/../Local/Google/Chrome/User Data/Local State", 'r') as file:
    encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
encrypted_key = base64.b64decode(encrypted_key)
encrypted_key = encrypted_key[5:]
decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"


def getFromFile(str):
    config = configparser.ConfigParser()
    config.read('cookies.ini')
    return config['cookies'][str]

def getCSRFToken(selection):
    if selection == 1:
        try:
            return getFromFile('csrftoken')
        except:
            if not os.path.exists('cookies.ini'):
                print('Creating cookies config file..')
                config = configparser.ConfigParser()
                config['cookies'] = {}
                with open('cookies.ini', 'w') as file:
                    config.write(file)
            pass
    csrftoken = getCookie('leetcode.com', 'csrftoken')
    config = configparser.ConfigParser()
    config.read('cookies.ini')
    config['cookies']['CSRFTOKEN'] = csrftoken
    with open('cookies.ini', 'w') as file:
        config.write(file)
    return csrftoken

def getLeetcodeSession(selection):
    if selection == 1:
        try:
            return getFromFile('leetcode_session')
        except:
            if not os.path.exists('cookies.ini'):
                print('Creating cookies config file..')
                config = configparser.ConfigParser()
                config['cookies'] = {}
                with open('cookies.ini', 'w') as file:
                    config.write(file)
            pass

    leetcode_session = getCookie('.leetcode.com', 'LEETCODE_SESSION')
    config = configparser.ConfigParser()
    config.read('cookies.ini')
    config['cookies']['LEETCODE_SESSION'] = leetcode_session
    with open('cookies.ini', 'w') as file:
        config.write(file)
    return leetcode_session

def getCookie(host, targetName):
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    conn = sqlite3.connect(cookiepath)
    conn.text_factory = bytes     #lambda x : str(x, 'latin1')
    cu=conn.cursor()
    for host_key,name, encrypted_value in cu.execute(sql).fetchall():
        try:
            # Try to decrypt as AES (2020 method)
            cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=encrypted_value[3:3+12])
            decrypted_value = cipher.decrypt_and_verify(encrypted_value[3+12:-16], encrypted_value[-16:])
        except:
            # If failed try with the old method
            decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8') or value or 0
        if targetName == name.decode('utf-8'):
            return decrypted_value.decode('utf-8')

