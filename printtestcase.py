import os, json, sys
def printTestCase():
    try:
        input = sys.argv

        try:
            testcase_file = input[1]
        except Exception as err:
            print(err)
            return
        with open('testcases/' + testcase_file + '.json') as file:
            data = json.load(file)
        for key in data:
            print(key)
            print(data[key])
            print('...')
    except Exception as err:
        print(err)
        return

printTestCase()