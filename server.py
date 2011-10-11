import sys, os, time, atexit
from signal import SIGTERM
from dbApi import dbApi
from ConfigParser import ConfigParser

CURRENT_DIR = os.getcwd() + '/' # current dir with slas

class Server:
	"""This is a main initialization class
	Here we will have all main initialization functions and objects"""

	def __init__(self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.data = {}
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr

		# Configuration import
		config = ConfigParser()
		config.readfp(open(CURRENT_DIR + 'include/' + 'mong.conf', 'rb'))
		# Append to data stack

#		self.pidfile = config.get('Server', 'pidfile')

		# Database initialization
		host = config.get('Database', 'host')
		user = config.get('Database', 'user')
		passwd = config.get('Database', 'passwd')
		dbname = config.get('Database', 'dbname')
		db = dbApi(host, user, passwd, dbname)

		# Setting up the pid file
		pidfile = config.get('Server', 'pidfile')
		self.pidfile = pidfile

		# Append to data stack
		self.data['database'] = db
		self.data['config'] = config
		self.data['pidfile'] = pidfile

	def daemonize(self):
		"""
		UNIX double-fork magic. Some info:		
		Fork a second child and exit immediately to prevent zombies.  This
		causes the second child process to be orphaned, making the init
		process responsible for its cleanup.  And, since the first child is
		a session leader without a controlling terminal, it's possible for
		it to acquire one by opening a terminal in the future (System V-
		based systems).  This second fork guarantees that the child is no
		longer a session leader, preventing the daemon from ever acquiring
		a controlling terminal.
		"""

		try:
			pid = os.fork()
			if pid > 0:
				# exit first parrent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1: failed: %d (%s)\n" % (e.errno, e.sdrerror))
			sys.exit(1)

		# decouple from parrent environment
		os.chdir('/')
		os.setsid()
		os.umask(0)

		# do second fork
		try:
			pid = os.fork()
			if pid > 0:
		# exit from second parrent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #2: failed: %d (%s)\n" % (e.errno, e.sdrerror))
			sys.exit(1)

		# redirect standart file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdin.fileno())
		os.dup2(se.fileno(), sys.stdin.fileno())

		# write pid file
		atexit.register(self.delpid)
		pid = str(os.getpid())
		self.pid = pid
		file(self.pidfile, 'w+').write("%s\n" % pid)

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for pid file to see if the daemon already runs
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if pid:
			message = "pidfile %s already exist, maybe Mongrel already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)

		# Start the daemon
		self.daemonize()
		sys.stderr.write("Starting %s ... PID: %s\n" % (self.pidfile, self.pid))
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from pidfile
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist, maybe Mongrel not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not and error in restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
				else:
					print str(err)
					sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()
	
	def status(self):
		"""
		Get status information
		"""
		# Get the pid from pidfile
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist, maybe Mongrel not running?\n"
			sys.stderr.write(message % self.pidfile)
		else:	
			sys.stdout.write("Status: Running! PID %s\n" % pid)

	def run(self):
		pass
