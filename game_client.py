from __future__ import with_statement
import xmlrpc.client 
from xmlrpc.server import * 
from _thread import start_new_thread
import hashlib
import Pyro4
from Pyro4 import threadutil

"""
gs = xmlrpc.client.ServerProxy("http://localhost:35673",verbose=False)
login = gs.login(hashlib.sha224("peztest".encode("utf-8")).hexdigest())
print(login)
"""
class c_handler(object):
	@Pyro4.callback
	def sys(self,msg):
		print(msg)	
	


class Client(object):
	def __init__(self):
		self.game = Pyro4.core.Proxy("PYRO:game@localhost:35674")
		self.exit = False
		self.ch = c_handler()
	def start(self):
		print(self.game.get_sector_info())
		print(self.game.get_user_info("rrr",self.ch))

class DaemonThread(threadutil.Thread):
	def __init__(self, client):
		threadutil.Thread.__init__(self)
		self.client = client
		self.setDaemon(True)
	def run(self):
		daemon = Pyro4.core.Daemon()
		daemon.register(self.client)
		daemon.requestLoop(lambda: not self.client.exit)
global client
def setup():
	global client
	client = Client()
	daemonthread=DaemonThread(client)
	daemonthread.start()
	client.start()
if(__name__ == "__main__"):
	setup()

