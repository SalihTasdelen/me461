from math import *

def eval_args(args):	
	'''
	bugeval helps you to evaluate or execute single line python commands
	BUT, you need to pass at least one argument to evaluate or execute
	You can pass any number of:
		phtyon commands given in seperate quotes
		or arithmetic operations
		Example:
				bugeval "sum([x for x in range(0,100)])" 9*14-45
	'''
	
	for current_arg in args:
		try:
			res = eval(current_arg)
			return "{0} evalates to {1}".format(current_arg, res)
		except:
			try:
				exec(current_arg)
				return "Executing {0}".format(current_arg)
			except:
				return "{0} did not evaluate or execute :(".format(current_arg)