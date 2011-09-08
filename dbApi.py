import MySQLdb

class dbApi(object):
	"""Main database class
		call: db = dbApi(host, user, passwd, name)
	"""
	def __init__(self, dbhost, dbuser, dbpass, dbname):
		self.dbhost = dbhost
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbname = dbname
		# Init the connection
		self._connection()

	def _connection(self):
		try:
			self.conn = MySQLdb.connect(host = self.dbhost,
									user = self.dbuser,
									passwd = self.dbpass,
									db = self.dbname
									)
			self.cursor = self.conn.cursor()
		except MySQLdb.Error, e:
			print "Error %d : %s" % (e.args[0], e.args[1])
			
	def select(self, query):
		if self.cursor is None:
			self.connection()
		try:
			self.cursor.execute(query)
			return self.cursor
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

	def insert(self, query):
		if self.cursor is None:
			self.connection()
		try: 
			self.cursor.execute(query)
			if self.cursor is not None:
				self.conn.commit()
			return self.cursor
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

	def disconnect(self):
		try:
			self.conn.close()
		except MySQLdb.Error, e:  
			print "Error %d: %s" % (e.args[0], e.args[1])


if __name__ == "__main__":
	db = dbApi('localhost', 'root', 'null02', 'mongrel')
	q = db.select("SELECT * FROM users")
	result = q.fetchall()
	print result[0][1]
