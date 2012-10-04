#import xmlrpc.client 
#from xmlrpc.server import * 
from _thread import start_new_thread
#import hashlib
#import sys
import time
import Pyro4
from Pyro4 import threadutil

"""
gs = xmlrpc.client.ServerProxy("http://localhost:35673",verbose=False)
login = gs.login(hashlib.sha224("peztest".encode("utf-8")).hexdigest())
print(login)
"""

class Chatter(object):
	def __init__(self):
		#self.game = Pyro4.core.Proxy("PYRO:Game@localhost:35674")
		self.game = Pyro4.core.Proxy("PYRO:Game@openstrike.de:35674")
		self.exit = False
	def sys(self,msg):
		print(msg)	
	def start(self):
		si = self.game.get_sector_info()
		print(si)
		ui = self.game.join("rrr","n",self)
		print(ui)

class DaemonThread(threadutil.Thread):
	def __init__(self):
		threadutil.Thread.__init__(self)
		#self.chatter = chatter
		self.setDaemon(True)
		#daemon.register(self.chatter)
	def run(self):
		chatter.start()
		"""with Pyro4.core.Daemon() as daemon:
			print("registered object")
			daemon.requestLoop(lambda: not self.chatter.exit)
		"""
		"""daemon = Pyro4.core.Daemon()
		daemon.register(self.chatter)
		daemon.requestLoop(lambda: not self.chatter.exit)
		"""

chatter = Chatter()

daemon = Pyro4.core.Daemon(host="localhost",port=35675)
print(daemon.locationStr)
print(daemon.natLocationStr)
daemon.register(chatter)
daemonthread=DaemonThread()
daemonthread.start()
daemon.requestLoop(lambda: not chatter.exit)
