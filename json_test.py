import json

t = {"pow" :(121,32,"wewaea!","i")}

class test():
	def __init__(self):
		self.x = 12
#t = test()
d = json.dumps(t)
f = json.loads(d)
#print(f.x)
#f.join()
#print(f.x)
print(f)
