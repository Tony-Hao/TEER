from datetime import datetime

# define the script global logger
def get_now ():
	tnow = datetime.now()
	return tnow

def get_difference(t1, t2):
	td = t2 - t1
	return td
