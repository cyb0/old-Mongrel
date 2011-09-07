#!/usr/bin/env python

def info(object, spacing=10, collapse=1):
	"""Print methods and doc strings.
	
	Take module, class, list, dictionary, or string."""
	methodList = [method for method in dir(object) if callable(getattr(object, method))]
	processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)	
	print "\n".join(["%s %s" % (method.ljust(spacing), processFunc(str(getattr(object, method).__doc__))) for method in methodList])

def output(data, format="text"):
	"""An example of polymorphism in Python."""
	output_function = getattr(apihelper, "output_%s" % format)
	print output_function
									
if __name__ == "__main__":
        print info.__doc__
								
