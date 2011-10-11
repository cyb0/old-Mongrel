import sys, os, time
from server import Server
from poller import Poller

CURRENT_DIR = os.getcwd() + '/' # current dir with slas

class Mongrel(Server):
	def run(self):
		while True:
			time.sleep(1)

# UGLY CALL!!!
app = Mongrel(stdout = CURRENT_DIR + 'logs/' + 'output.log', stderr = CURRENT_DIR + 'logs/' + 'error.log')
#print len(app.data)
if len(sys.argv) == 2:
	if 'start' == sys.argv[1]:
		app.start()
		app.status()
	elif 'stop' == sys.argv[1]:
		app.stop()
	elif 'restart' == sys.argv[1]:
		app.restart()
	else:
		print "Unknown command\n"
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

#poller = Poller(app.data, 'tmp/mongrel-poller.pid')
#poller.start()
