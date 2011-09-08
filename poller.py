import sys, os, time
from server import Server

class Poller(Server):
	"""This is the main poller class
	Here will have to do a lot of work, 
	but first have to check some things
	"""

	def __init__(self, obj, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.data = {}
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
		
		if obj is not None:
			self.data = obj
			# Init database descriptor
			db = self.data['database']
			# q = db.select("SELECT * FROM users")
			# result = q.fetchall()
			# print result[0][1]
	def run(self):
		while True:
			time.sleep(1)
					

