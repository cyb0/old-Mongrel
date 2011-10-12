import sys, os, time
from server import Server
from include.telnet import TelnetServer

CURRENT_DIR = os.getcwd() + '/' # current dir with slas

client_list = []

class Mongrel(Server):

	def mon_connect(self, client):
		# TODO: Some log file append will be good
		print "++ Opened connection from %s \n" % client.addrport()
		# TODO: Broadcast function call should be here if any
		client_list.append(client)
		client.active = True
		client.send("Welcome to Mongrel v0.2. Your IP is %s \n" % client.addrport())
		client.send("Your terminal type is %s \n" % client.terminal_type)
		client.send(">>> ")
				
	def mon_disconnect(self, client):
		print "++ Closed connection from %s \n" % client.addrport()
		client.send("Bye, %s!" % client.addrport())
		client_list.remove(client)
		client.active = False

	def process_client(self):
		for client in client_list:
			if client.active and client.cmd_ready:
				self.chat(client)

	def chat(self, client):
		"""
		Log everything that the user writes
		"""
		msg = client.get_command()
		for guest in client_list:
			if guest != client:
				guest.send("%s: %s\n" % (client.addrport(), msg))
				guest.send(">>> ")
			else:
				guest.send("%s: %s\n" % (client.addrport(), msg))
				client.send(">>> ")
		cmd = msg.lower()
		# if cmd == 'cl':
		# Disconnect
		if cmd == 'bye':
			client.active = False

	def telnet_conn(self):

		self.server_conn = TelnetServer(
			port = self.port,
			address = '',
			on_connect = self.mon_connect,
			on_disconnect = self.mon_disconnect
		)

		# self.server_conn.on_connect = self.mon_connect
		# self.server_conn.on_disconnect = self.mon_disconnect

		sys.stdout.write("Running telnet service on port %d \n" % self.port)
		while (1):
			self.server_conn.poll()
			self.process_client()

	def run(self):
		self.telnet_conn()
		while True:
			time.sleep(1)

# UGLY CALL!!!
app = Mongrel(stdout = CURRENT_DIR + 'logs/' + 'output.log', stderr = CURRENT_DIR + 'logs/' + 'error.log')
if len(sys.argv) == 2:
	if 'start' == sys.argv[1]:
		app.start()
		app.status()
	elif 'stop' == sys.argv[1]:
		app.stop()
	elif 'restart' == sys.argv[1]:
		app.restart()
	elif 'status' == sys.argv[1]:
		app.status()
	else:
		print "Unknown command\n"
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

#poller = Poller(app.data, 'tmp/mongrel-poller.pid')
#poller.start()



# app = Mongrel(stdout = CURRENT_DIR + 'logs/' + 'output.log', stderr = CURRENT_DIR + 'logs' + 'error.log')
