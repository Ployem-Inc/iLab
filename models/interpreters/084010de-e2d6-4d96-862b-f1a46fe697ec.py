if __name__ == '__main__':
	import io
	import traceback
	try:
		while 1: print(9)
		print('#$$##@*run_over$$##@*')
	except Exception as e:
		errors = io.StringIO()
		traceback.print_exc(file=errors)
		content = str(errors.getvalue())
		content = content.replace('\n','!$$^^new_line$$@#@')
		print('*$$##Error$$##!\t%s' % (content))
		errors.close()