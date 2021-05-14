import requests, json, time, hashlib
from http.cookies import SimpleCookie

import requests, json
from http.cookies import SimpleCookie
import getCookie
import os

def getAllCookie():
    csrftoken = ''
    leetcode_session = ''
    try:
        csrftoken = getCookie.getCSRFToken()
        leetcode_session = getCookie.getLeetcodeSession()
        print('successfully loaded cookies..')
    except Exception as err:
        print(err)
        print('[lc_submission] error loading cookies file..')
        return

    cookie_str = 'csrftoken=' + csrftoken + ';LEETCODE_SESSION=' + leetcode_session
    return [csrftoken, leetcode_session, cookie_str]


def toStr(item):
    if isinstance(item, list): return '[' + ','.join([str(i) for i in item]) + ']'
    return str(item)

def myhash(item):
        return hashlib.sha256(bytes(toStr(item), 'utf-8')).hexdigest()

def genCode(var, inputlist, resultlist, default_answer):
    size = len(inputlist)
    codebody = ''
    for i in range(size):
        code_init = '\n        if '
        varsize = len(var)
        code_iter = []
        # if varsize > 1:
        for j in range(varsize):
            code_iter.append('myhash(' + var[j] + ') == "' + inputlist[i][j] + '"')
        # else:
        #     code_iter.append('myhash(' + str(var[0]) + ') == "' + inputlist[i] + '"')

        code_init += " and ".join(code_iter)
        code_init += ': return ' + resultlist[i]
        codebody += code_init
    codebody += '\n        return ' + default_answer
    return codebody

def getQuestionSlug(url):
    split = url.split("/")
    return split[4]

def loadQuestionMetaData():
    map = {}
    with open('metadata.json', 'r') as file:
        map = json.load(file)
    return map

def submit(questionNum, methodSignature, vars, defaultInput):

    inputlist = []
    encrypted_inputlist = []
    resultlist = []
    metadata = loadQuestionMetaData()

    questionURL = 'https://leetcode.com/problems/'
    frontend_question_id = questionNum
    questionNum = str(questionNum)
    questionURL += metadata[questionNum]['question_slug'] + '/submit/'

    csrftoken = ''
    cookie_str = ''

    try:
        cookies = getAllCookie()
        csrftoken = cookies[0]
        cookie_str = cookies[2]
    except:
        print('Error loading cookie file.. exit now')

    headers = {
        'referer': 'https://leetcode.com/accounts/login/',
        'cookie' : cookie_str,
        'x-csrftoken' : csrftoken
    }

    dir = os.path.dirname(__file__) + '/testcases/'
    if not os.path.exists(dir): os.mkdir(dir)
    questionNum = metadata[questionNum]['question_id']

    testCases = dir + str(frontend_question_id) + '.json'

    map = {}
    if os.path.exists(testCases):
        with open(testCases, 'r') as file:
            map = json.load(file)
    for key in map:
        tmpList = []
        for item in key.split('\n'):
            tmpList.append(myhash(item.rstrip()))
        encrypted_inputlist.append(tmpList)
        resultlist.append(map[key])

    # print(map)

    count = 0
    try:
        while True:

            count += 1
            code_head = """import hashlib\ndef toStr(item): \n    if isinstance(item, list): return '[' + ','.join([toStr(i) for i in item]) + ']'\n    return str(item)\ndef myhash(item): return hashlib.sha256(bytes(toStr(item),"utf-8")).hexdigest()\nclass Solution:\n    """
            code_head += methodSignature
            code_body = ''
            code_tail = ''

            code_body = genCode(vars, encrypted_inputlist, resultlist, defaultInput)
            code = code_head + code_body + code_tail

            param = {
                'lang': "python3",
                'question_id': questionNum,
                'typed_code': code
            }

            print('Submitting now', end='', flush=True)
            while True:
                resp = requests.post(url = questionURL, data = json.dumps(param), headers = headers)
                time.sleep(1)
                # print(resp.text)
                # print(resp.status_code)
                if resp.status_code == 499:
                    print('leetcode closed drequest')
                    return
                if resp.status_code == 405:
                    print('error in input..')
                    return
                if resp.status_code == 403:
                    print('user is not logged in.. please update cookies file')
                    try: os.remove('cookies.ini')
                    except: pass
                    return
                if resp.status_code == 200: break
                else:
                    if resp.status_code == 429:
                        print('.', end = '', flush=True)

            resultj = json.loads(resp.text)

            try:
                submission_result = resultj['submission_id']
            except:
                print('error loading submission id.. error msg from leetcode..')
                print(resultj)
                return
            # print(resultj)
            submission_id = resultj['submission_id']

            checkURL_head = 'https://leetcode.com/submissions/detail/'
            checkURL_append = '/check/'
            checkURL = checkURL_head + str(submission_id) + checkURL_append

            print(checkURL_head + str(submission_id))

            checkCookie = {
                'cookie': cookie_str,
                'x-csrftoken' : csrftoken
            }

            resp = ''
            print('Fetching result', end='', flush=True)
            while True:
                resp = requests.get(url = checkURL, cookies = checkCookie)
                submission_result = json.loads(resp.text)
                time.sleep(1)
                print(resp.text)
                if submission_result['state'] != 'PENDING' and submission_result['state'] != 'STARTED': break
                else:
                    print('.', end='', flush=True)


            submission_resp = json.loads(resp.text)

            print('%dth submission result.. %s' % (count, submission_resp['status_msg']))

            if submission_resp['status_msg'] == 'Accepted': break

            # print('incorrect test case..\n' + submission_resp['last_testcase'])
            # print('expected output..' + submission_resp['expected_output'])

            inputs = submission_resp['last_testcase']
            inputssplit = inputs.split("\n")
            newInputList = []
            for eachinput in inputssplit:
                eachinput = eachinput.replace('"', '')
                newInputList.append(myhash(eachinput))
            inputlist.append(inputs)
            outputs = submission_resp['expected_output']
            encrypted_inputlist.append(newInputList)
            resultlist.append(outputs)
            if inputs in map:
                print('Found same results .. submission stopped')
                return
            map[inputs] = outputs
            with open(testCases, 'w') as file:
                json.dump(map, file)

    except Exception as err:
        print(err)
        pass



