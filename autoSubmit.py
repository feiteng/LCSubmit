import sys, configparser, submissionMask




input = sys.argv
# print(input)
submissionFile = input[1]
config = configparser.ConfigParser()
# print(config)
config.read(submissionFile)
question_id = int(config['params']['question_id'])
function_signature = config['params']['function_signature']
default_input = config['params']['default_input']

submissionMask.submit(question_id, function_signature, default_input)



