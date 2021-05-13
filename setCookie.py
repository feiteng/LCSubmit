import os, configparser
import json
import base64
import sqlite3
from shutil import copyfile
import requests, json
from bs4 import BeautifulSoup
import sqlite3
import gzip, os

from Cryptodome.Cipher import AES



def getCookie(host, targetName):

    import win32crypt
    encrypted_key = None
    try:
        with open(os.getenv("APPDATA") + "/../Local/Google/Chrome/User Data/Local State", 'r') as file:
            encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
        encrypted_key = base64.b64decode(encrypted_key)
        encrypted_key = encrypted_key[5:]
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        print('error in locating chrome cookie file.. please input manually')

    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"

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

def setCookie():
    if os.path.exists('cookies.ini'):
        os.rmdir('cookies.ini')

    csrftoken = getCookie('leetcode.com', 'csrftoken')
    leetcode_session = getCookie('.leetcode.com', 'LEETCODE_SESSION')

    config = configparser.ConfigParser()
    config['cookies'] = {}
    config['cookies']['CSRFTOKEN'] = csrftoken
    config['cookies']['LEETCODE_SESSION'] = leetcode_session
    with open('cookies.ini', 'w') as file:
        config.write(file)