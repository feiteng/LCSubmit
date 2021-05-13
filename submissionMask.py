import requests, json, time, hashlib
from http.cookies import SimpleCookie

import requests, json
from http.cookies import SimpleCookie
import getCookie
import os
import lc_submission

def parseInput(s : str):
    re = []
    initialPos = s.index('(')
    lastPos = s.index(')')
    substring = s[initialPos + 1:lastPos]
    # print(substring)
    items = substring.split(",")
    size = len(items)
    for i in range(1, size):
        re.append(items[i].split(":")[0].strip())

    return re
def parseDefaultInput(s : str):
    initialPos = s.index('->')
    vartype = s[initialPos + 3 : len(s) - 1]
    map = {'int':'0','List[int]':'[]'}
    return map[vartype]


def submit(questionNum, methodSignature, defaultInput):
    vars = parseInput(methodSignature)
    # defaultInput = parseDefaultInput(methodSignature)

    lc_submission.submit(questionNum=questionNum, methodSignature=methodSignature, vars = vars, defaultInput=defaultInput)