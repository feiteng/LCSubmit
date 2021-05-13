import os, configparser

# import setCookie

def getFromFile(str):
    config = configparser.ConfigParser()
    config.read('cookies.ini')
    return config['cookies'][str]

def getCSRFToken():
    # if selection == 1:
    try:
        return getFromFile('CSRFTOKEN')
    except:
        print('adjust your cookie file properly..')
        # setCookie.setCookie()
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
        print('adjust your cookie file properly..')
        # setCookie.setCookie()
        # if not os.path.exists('cookies.ini'):
        #     print('Creating cookies config file..')
        #     config = configparser.ConfigParser()
        #     config['cookies'] = {}
        #     with open('cookies.ini', 'w') as file:
        #         config.write(file)



