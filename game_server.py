from __future__ import with_statement
from xmlrpc.server import * 
import xmlrpc.client 
from _thread import start_new_thread
import Pyro4
import hashlib
import game_client

class game(object):
	def get_sector_info(self):
		return((1,1))
	def get_user_info(self,session_id,game_client):
		self.gc = game_client
		print(session_id)
		self.gc._pyroOneway.add("sys")
		sysmsg("server online")
		#game_client.sys("server online")
		return(("hi","aodoo",123))
	def sysmsg(self,msg):
		self.gc.sys(msg)
		

def login(hash):
	print(hash)
	return(True)

def setup():
	server = SimpleXMLRPCServer(("localhost",35673),logRequests=False)
	server.register_function(login)
	start_new_thread(server.serve_forever,())
	daemon = Pyro4.core.Daemon(host="localhost",port=35674)
	uri=daemon.register(game(),objectId="game")
	daemon.requestLoop()
setup()