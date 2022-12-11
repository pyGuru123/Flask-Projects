from src.services import *
from src.pythonREPL import *
from timeit import default_timer as timer

def parseMessage(msg):
	print(msg)
	message = msg.get("message", None)
	if message:
		if 'chat' in message.keys() and 'text' in message.keys():
			chatId = message['chat']['id']
			text = message['text'].strip('\n').strip()
			return chatId, text
	return None, None

def parseCommand(text, debug=False):
	if text.startswith('/runpy'):
		code = text.replace('/runpy', '').strip('\n').strip()
		if '-d' in code:
			code = code.replace('-d', '').strip('\n').strip()
			debug=True

		# output = CodeExecuter(code).execute_python
		# if debug:
		# 	result = f"Result \n{output[1][-1]}"
		# else:
		# 	result = f"Execution Results \n\
		# 	Execution time: {output[0]:.6f}s \n\
		# 	Return Code: {output[-1]} \n\
		# 	Errors: {output[1][0] if output[1][0] != '' else None} \n\
		# 	Output: {output[1][-1]}"		

		try:
			executor = CodeExecutor2()
			start = timer()
			output = executor.execute_python(code)
			end = timer()
		except Exception as e:
			return "Runtime Error"
		
		if debug:
			result = f"Result \n{output}Execution time: {end-start:.6f}s \n"
		else:
			result = f"Result \n{output}"
		return result

	elif text.startswith('/date'):
		return get_date()
	elif text.startswith('/time'):
		return get_time()
	elif text.startswith('/quote'):
		return get_quote()
	elif text.startswith('/about'):
		return """This bot is written by Prajjwal Pathak.
		Repo : https://github.com/pyGuru123/pyBot"""
	elif text.startswith('/youtube'):
		return "https://www.youtube.com/c/pyGuru"
