import sys, configparser, submissionMask, os, platform, setCookie

def submit():
    try:
        if not os.path.exists('cookies.ini'):
            print('Cookie file does not exist, configure it please..')
            if platform.system() == 'Windows':
                setCookie.setCookie()
            # setCookie.setCookie()
        input = sys.argv
        # print(input)
        try:
            submissionFile = input[1]
        except:
            print('error loading question config file.. default to s1.ini')
            submissionFile = 's1.ini'
        config = configparser.ConfigParser()
        # print(config)
        config.read(submissionFile)
        question_id = int(config['params']['question_id'])
        function_signature = config['params']['function_signature']
        default_input = config['params']['default_input']

        submissionMask.submit(question_id, function_signature, default_input)
    except:
        return

submit()