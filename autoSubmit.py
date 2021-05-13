import sys, configparser, submissionMask


submissionFile = 's1.ini'
try:
    input = sys.argv
    print(input)
    submissionFile = input[2]
except:
    pass



config = configparser.ConfigParser()
print(config)
config.read(submissionFile)
print(config.sections())

question_id = int(config['params']['question_id'])
function_signature = config['params']['function_signature']
default_input = config['params']['default_input']


submissionMask.submit(question_id, function_signature, default_input)