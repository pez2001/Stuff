from __future__ import with_statement
from xmlrpc.server import * 
import xmlrpc.client 
from _thread import start_new_thread
import Pyro4
import hashlib
#import game_client

class Game(object):
	def __init__(self):
		self.users = {}
		self.channels={}        # registered channels { channel --> (nick, client callback) list }
		self.nicks=[]            # all registered nicks on this server
	def getChannels(self):
		return list(self.channels.keys())
	def getNicks(self):
		return self.nicks
		
	def get_sector_info(self):
		return((1,1))
		
	def join(self,channel,nick,callback):
		if not channel or not nick:
			raise ValueError("invalid channel or nick name")
		if nick in self.nicks:
			raise ValueError('this nick is already in use')
		if channel not in self.channels:
			print('CREATING NEW CHANNEL %s' % channel)
			self.channels[channel]=[]
		self.channels[channel].append((nick, callback))
		self.nicks.append(nick)
		self.gc = callback
		callback._pyroOneway.add('message')    # don't wait for results for this method
		print("%s JOINED %s" % (nick, channel))
		self.publish(channel,'SERVER','** '+nick+' joined **')
		return [nick for (nick,c) in self.channels[channel]]  # return all nicks in this channel

		"""self.channels[channel].append((nick, callback))
		self.nicks.append(nick)
		callback._pyroOneway.add('message')    # don't wait for results for this method
		callback.message(nick,"hi")    # oneway call
		return(("1","2"))
		#return [nick for (nick,c) in self.channels[channel]]  # return all nicks in this channel
		"""
		
	def get_user_info(self,session_id,callback):
		self.gc = callback
		print(session_id)
		self.gc._pyroOneway.add("sys")
		sysmsg("server online")
		#game_client.sys("server online")
		return(("hi","aodoo",123))
	def sysmsg(self,msg):
		self.gc.sys("server",msg)
	def publish(self,c,n,msg):
		self.gc.message("server",msg)
		

def login(hash):
	print(hash)
	return(True)

def setup():
	"""server = SimpleXMLRPCServer(("localhost",35673),logRequests=False)
	server.register_function(login)
	start_new_thread(server.serve_forever,())
	"""
	daemon = Pyro4.core.Daemon(host="localhost",port=35674)
	uri=daemon.register(Game(),objectId="Game")
	daemon.requestLoop()
setup()