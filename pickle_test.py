import pickle

class test():
	def __init__(self):
		self.x = 12
	def join(self):
		self.x = 13

x = (12,"3wewe","3332")
t = x
d = pickle.dumps(t)
#print(d)
e = pickle.loads(d)
print(e)

t = test()
d = pickle.dumps(t)
f = pickle.loads(d)
print(f.x)
f.join()
print(f.x)
