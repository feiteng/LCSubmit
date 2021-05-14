import os, configparser

# import setCookie

def getFromFile(str):
    config = configparser.ConfigParser()
    try:
        config.read('cookies.ini')
    except Exception as err:
        print(err)
        print('Error finding cookies config file')
        return '#'
    return config['cookies'][str]

def getCSRFToken():
    # if selection == 1:
    try:
        return getFromFile('CSRFTOKEN')
    except:
        return '#'

def getLeetcodeSession():
    # if selection == 1:
    try:
        return getFromFile('LEETCODE_SESSION')
    except:
        return '#'

