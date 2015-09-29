#!/usr/bin/env python
import os
import pygame
import pygame.gfxdraw
import random
import math
"""globals"""
image_dir = "./images"
screen = None
tex = None
knot = None

class Letter():
	def __init__(self,letter):
		if(letter == "s"):
			self.vertices = []
			self.vertices.append(Vector(10,0,0))
			self.vertices.append(Vector(2,0,0))
			self.vertices.append(Vector(1,-2,0))
			self.vertices.append(Vector(2,-4,0))
			self.vertices.append(Vector(8,-6,0))
			self.vertices.append(Vector(9,-8,0))
			self.vertices.append(Vector(8,-10,0))
			self.vertices.append(Vector(0,-10,0))
		if(letter == "t"):
			self.vertices = []
			self.vertices.append(Vector(10,0,0))
			self.vertices.append(Vector(0,0,0))
			self.vertices.append(Vector(5,0,0))
			self.vertices.append(Vector(5,-10,0))

		if(letter == "e"):
			self.vertices = []
			self.vertices.append(Vector(10,0,0))
			self.vertices.append(Vector(0,0,0))
			self.vertices.append(Vector(0,-5,0))
			self.vertices.append(Vector(5,-5,0))
			self.vertices.append(Vector(0,-5,0))
			self.vertices.append(Vector(0,-10,0))
			self.vertices.append(Vector(10,-10,0))

		if(letter == "p"):
			self.vertices = []
			self.vertices.append(Vector(10,0,0))
			self.vertices.append(Vector(0,0,0))
			self.vertices.append(Vector(0,-10,0))
			self.vertices.append(Vector(0,-5,0))
			self.vertices.append(Vector(10,-5,0))
			self.vertices.append(Vector(10,0,0))

		if(letter == "h"):
			self.vertices = []
			self.vertices.append(Vector(0,0,0))
			self.vertices.append(Vector(0,-10,0))
			self.vertices.append(Vector(0,-5,0))
			self.vertices.append(Vector(10,-5,0))
			self.vertices.append(Vector(10,-10,0))
			self.vertices.append(Vector(10,0,0))

		if(letter == "i"):
			self.vertices = []
			self.vertices.append(Vector(2,0,0))
			self.vertices.append(Vector(2,-10,0))

		if(letter == "heart"):
			self.vertices = []
			self.vertices.append(Vector(5,-3,0))
			self.vertices.append(Vector(7,-2,0))
			self.vertices.append(Vector(9,-1,0))
			self.vertices.append(Vector(10,-2,0))
			self.vertices.append(Vector(5,-10,0))
			self.vertices.append(Vector(0,-2,0))
			self.vertices.append(Vector(1,-1,0))
			self.vertices.append(Vector(3,-2,0))
			self.vertices.append(Vector(5,-3,0))

	def Draw(self,offset):
		global screen,rot
		#for v in self.vertices:
		#		d = v + offset
		#		d.Draw(pygame.Color("white"))
		for i in range(len(self.vertices)-1):
			d = Vector(-5,0,0)
			a = self.vertices[i]
			a = a + d
			a = a.RotateY(rot*10)
			a= a + offset
			b = self.vertices[i+1]
			b = b +d
			b = b.RotateY(rot*10)
			b = b + offset
			da = a.Project()
			db = b.Project()
			x1 = int(da.x)
			y1 = int(da.y)
			x2 = int(db.x)
			y2 = int(db.y)
			if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
				if(x2>0 and x2<screen.get_width() and y2>0 and y2<screen.get_height()):
					pygame.gfxdraw.line(screen, x1,y1,x2,y2, pygame.Color("white"))



class TriFace():
	def __init__(self,p1,p2,p3):
		self.vertices = [p1,p2,p3]

	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(TriFace(a.vertices[0]*b,a.vertices[1]*b,a.vertices[2]*b))

	def Draw(self,offset):
		global screen,rot
		a = self.vertices[0]
		b = self.vertices[1]
		c = self.vertices[2]
		a = a.RotateY(rot*10)
		b = b.RotateY(rot*10)
		c = c.RotateY(rot*10)
		a = a + offset
		b = b + offset
		c = c + offset
		da = a.Project()
		db = b.Project()
		dc = c.Project()
		x1 = int(da.x)
		y1 = int(da.y)
		x2 = int(db.x)
		y2 = int(db.y)
		x3 = int(dc.x)
		y3 = int(dc.y)
		if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
			if(x2>0 and x2<screen.get_width() and y2>0 and y2<screen.get_height()):
				pygame.gfxdraw.line(screen, x1,y1,x2,y2, pygame.Color("white"))
		if(x2>0 and x2<screen.get_width() and y2>0 and y2<screen.get_height()):
			if(x3>0 and x3<screen.get_width() and y3>0 and y3<screen.get_height()):
				pygame.gfxdraw.line(screen, x2,y2,x3,y3, pygame.Color("white"))
		if(x3>0 and x3<screen.get_width() and y3>0 and y3<screen.get_height()):
			if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
				pygame.gfxdraw.line(screen, x3,y3,x1,y1, pygame.Color("white"))
		pygame.gfxdraw.filled_trigon(screen,x1,y1,x2,y2,x3,y3,pygame.Color("red"))
		#pygame.gfxdraw.textured_polygon(screen,[[x1,y1],[x2,y2],[x3,y3]],screen,0,0)

class QuadFace():
	def __init__(self,p1,p2,p3,p4):
		self.vertices = [p1,p2,p3,p4]

	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(QuadFace(a.vertices[0]*b,a.vertices[1]*b,a.vertices[2]*b,a.vertices[3]*b))

	def Draw(self,offset):
		global screen,rot,tex
		a = self.vertices[0]
		b = self.vertices[1]
		c = self.vertices[2]
		d = self.vertices[3]
		a = a.RotateY(rot*10)
		b = b.RotateY(rot*10)
		c = c.RotateY(rot*10)
		d = d.RotateY(rot*10)
		a = a + offset
		b = b + offset
		c = c + offset
		d = d + offset
		da = a.Project()
		db = b.Project()
		dc = c.Project()
		dd = d.Project()
		x1 = int(da.x)
		y1 = int(da.y)
		x2 = int(db.x)
		y2 = int(db.y)
		x3 = int(dc.x)
		y3 = int(dc.y)
		x4 = int(dd.x)
		y4 = int(dd.y)
		"""if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
			if(x2>0 and x2<screen.get_width() and y2>0 and y2<screen.get_height()):
				pygame.gfxdraw.line(screen, x1,y1,x2,y2, pygame.Color("white"))
		if(x2>0 and x2<screen.get_width() and y2>0 and y2<screen.get_height()):
			if(x3>0 and x3<screen.get_width() and y3>0 and y3<screen.get_height()):
				pygame.gfxdraw.line(screen, x2,y2,x3,y3, pygame.Color("white"))
		if(x3>0 and x3<screen.get_width() and y3>0 and y3<screen.get_height()):
			if(x4>0 and x4<screen.get_width() and y4>0 and y4<screen.get_height()):
				pygame.gfxdraw.line(screen, x3,y3,x4,y4, pygame.Color("white"))
		if(x4>0 and x4<screen.get_width() and y4>0 and y4<screen.get_height()):
			if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
				pygame.gfxdraw.line(screen, x4,y4,x1,y1, pygame.Color("white"))
		"""
		pygame.gfxdraw.filled_polygon(screen,[[x1,y1],[x2,y2],[x3,y3],[x4,y4]],pygame.Color("red"))
		#pygame.gfxdraw.textured_polygon(screen,[[x1,y1],[x2,y2],[x3,y3],[x4,y4]],tex,0,0)

class Point():
	def __init__(self,p1):
		self.vertex = p1

	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(Point(a.vertex*b))

	def Draw(self,offset):
		global screen,rot
		a = self.vertex
		a = a.RotateY(rot*10)
		a = a + offset
		da = a.Project()
		x1 = int(da.x)
		y1 = int(da.y)
		if(x1>0 and x1<screen.get_width() and y1>0 and y1<screen.get_height()):
			pygame.gfxdraw.pixel(screen,x1,y1,pygame.Color("red"))


class Mesh():
	def __init__(self,*faces):
		self.faces = faces
	def Draw(self,offset):
		for f in self.faces:
			f.Draw(offset)

class SceneObject():
	def __init__(self,mesh,pos,dir):
		self.mesh = mesh
		self.pos = pos
		self.dir = dir

class Scene():
	def __init__(self,camera,*objects):
		self.objects = objects
		self.camera = camera


class Camera():
	def __init__(self):
		pass

class Ray():
	def __init__(self):
		pass

class Light():
	def __init__(self):
		pass

class Matrix():
	def __init__(self):
		pass



class TriCube(Mesh):
	def __init__(self,size):
		#size is a float
		self.faces = []
		self.faces.append(TriFace(Vector(-1,-1,1),Vector(-1,-1,-1),Vector(1,-1,-1))*size)
		self.faces.append(TriFace(Vector(1,-1,-1),Vector(1,-1,1),Vector(-1,-1,1))*size)

		self.faces.append(TriFace(Vector(-1,1,1),Vector(-1,-1,1),Vector(1,-1,1))*size)
		self.faces.append(TriFace(Vector(1,-1,1),Vector(1,1,1),Vector(-1,1,1))*size)

		self.faces.append(TriFace(Vector(-1,1,1),Vector(-1,1,-1),Vector(1,1,-1))*size)
		self.faces.append(TriFace(Vector(1,1,-1),Vector(1,1,1),Vector(-1,1,1))*size)

		self.faces.append(TriFace(Vector(-1,1,-1),Vector(-1,-1,-1),Vector(1,-1,-1))*size)
		self.faces.append(TriFace(Vector(1,-1,-1),Vector(1,1,-1),Vector(-1,1,-1))*size)

		self.faces.append(TriFace(Vector(-1,1,-1),Vector(-1,-1,-1),Vector(-1,-1,1))*size)
		self.faces.append(TriFace(Vector(-1,-1,1),Vector(-1,1,1),Vector(-1,1,-1))*size)

		self.faces.append(TriFace(Vector(1,1,-1),Vector(1,-1,-1),Vector(1,-1,1))*size)
		self.faces.append(TriFace(Vector(1,-1,1),Vector(1,1,1),Vector(1,1,-1))*size)

class QuadCube(Mesh):
	def __init__(self,size):
		#size is a float
		self.faces = []
		self.faces.append(QuadFace(Vector(-1,-1,1),Vector(-1,-1,-1),Vector(1,-1,-1),Vector(1,-1,1))*size)
		self.faces.append(QuadFace(Vector(-1,1,1),Vector(-1,1,-1),Vector(1,1,-1),Vector(1,1,1))*size)
		self.faces.append(QuadFace(Vector(-1,1,1),Vector(-1,-1,1),Vector(1,-1,1),Vector(1,1,1))*size)
		self.faces.append(QuadFace(Vector(-1,1,-1),Vector(-1,-1,-1),Vector(1,-1,-1),Vector(1,1,-1))*size)
		self.faces.append(QuadFace(Vector(-1,1,-1),Vector(-1,-1,-1),Vector(-1,-1,1),Vector(-1,1,1))*size)
		self.faces.append(QuadFace(Vector(1,1,-1),Vector(1,-1,-1),Vector(1,-1,1),Vector(1,1,1))*size)


class TrefoilKnot(Mesh):
	def __init__(self,size):
		self.faces = []
		r = 0.5
		for i in range(0,200):
			x = ( math.sin(i) + 2*math.sin(2*i) ) #- 10
			y = ( math.cos(i) - 2*math.cos(2*i) ) #- 20
			z = ( -math.sin(3*i) ) #- 50
			x1 = x + r * math.cos(90*math.pi/180)
			y1 = y + r * math.sin(90*math.pi/180)
			x2 = x + r * math.cos(180*math.pi/180)
			y2 = y + r * math.sin(180*math.pi/180)
			x3 = x + r * math.cos(270*math.pi/180)
			y3 = y + r * math.sin(270*math.pi/180)
			x4 = x + r * math.cos(360*math.pi/180)
			y4 = y + r * math.sin(360*math.pi/180)
			#x = (2 + math.cos(3*i)) * math.cos(2*i)
			#y = (2 + math.cos(3*i)) * math.sin(2*i)
			#z = math.sin(3*i)
			self.faces.append(Point(Vector(x1,y1,z))*size)
			self.faces.append(Point(Vector(x2,y2,z))*size)
			self.faces.append(Point(Vector(x3,y3,z))*size)
			self.faces.append(Point(Vector(x4,y4,z))*size)



class Vector():
	def __init__(self, x = 0.0,y = 0.0,z = 0.0):
			self.x = x
			self.y = y
			self.z = z

	def __add__(a,b):
		return(Vector(a.x+b.x,a.y+b.y,a.z+b.z))

	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(Vector(a.x*b,a.y*b,a.z*b))
		else:
			return(Vector(a.x*b.x,a.y*b.y,a.z*b.z))


	def Draw(self,color):
		global screen
		s = self.Project()
		x = int(s.x)
		y = int(s.y)
		#print(x,y)
		if(x>0 and x<screen.get_width() and y>0 and y<screen.get_height()):
			screen.set_at((x,y),color)

	#def VecAngle(self,v):
	#	i = v-self
	#	o = Vector()
	#	return o

	def Print(self):
		print("X:",self.x," ,Y:",self.y," ,Z:",self.z)

	def Project(self):
			global screen
			fov = 90
			dist = 10
			v = Vector(self.x * fov / (self.z + dist) + screen.get_width()/2,-self.y * fov / (self.z + dist) + screen.get_height()/2,0)
			return v

	def RotateZ(self,angle):
		rad = angle * math.pi / 180
		v = Vector(self.x*math.cos(rad) - self.y*math.sin(rad),self.x*math.sin(rad) + self.y*math.cos(rad),self.z)
		return v

	def RotateX(self,angle):
		rad = angle * math.pi / 180
		v = Vector(self.x ,self.y*math.cos(rad) - self.z*math.sin(rad) ,self.y*math.sin(rad) + self.z*math.cos(rad))
		return v

	def RotateY(self,angle):
		rad = angle * math.pi / 180
		v = Vector(self.z*math.cos(rad) - self.x*math.sin(rad) ,self.y ,self.z*math.sin(rad) + self.x*math.cos(rad))
		return v

	def Rotate(self,xangle,yangle,zangle):
		radx = xangle * math.pi / 180
		rady = yangle * math.pi / 180
		radz = zangle * math.pi / 180
		v = Vector(self.x*math.cos(rad) - self.y*math.sin(rad),self.x*math.sin(rad) + self.y*math.cos(rad),self.z)
		v = Vector(v.x ,v.y*math.cos(rad) - v.z*math.sin(rad) ,v.y*math.sin(rad) + v.z*math.cos(rad))
		v = Vector(v.z*math.cos(rad) - v.x*math.sin(rad) ,v.y ,v.z*math.sin(rad) + v.x*math.cos(rad))
		return v



stars_num = 2000
stars = [None for x in range(stars_num)]
stars_old = [None for x in range(stars_num)]
dim = 2000
dimz = 1000

def generate_starfield(stars):
	global dim,dimz
	for i in range(int(len(stars))):
		stars[i] = Vector(random.randint(-dim,dim),random.randint(-dim,dim),random.randint(0,dimz))

def draw_stars(stars,angle):
	global screen,dimz
	screen.fill((0, 0, 0))
	for i in stars:
		#r = i.RotateZ(angle)
		#r = r.RotateX(angle)
		r = i.RotateZ(angle)
		r = r + Vector(0,0,-5)
		#r = i + Vector(-10,0,-35)
		c = int(255.0 * (1.0 - (i.z / dimz)))
		if(c<0):
			c = 0
		if(c>255):
			c = 255
		r.Draw(pygame.Color(c,c,c,c))

def move_stars(stars):
	global dim,dimz
	for i in stars:
		i.z -= 1.5
		#rad = r * math.pi / 180
		#i.x = i.x*math.cos(rad) - i.y*math.sin(rad)
		#iy = i.x*math.sin(rad) + i.y*math.cos(rad)
		if(i.z <= 10.0):
			#i.z = random.randint(dimz-100,dimz)
			i.z = dimz
			i.x = random.randint(-dim,dim)
			i.y = random.randint(-dim,dim)


rot = 0.0

def tick():
	global rot
	rot += 0.3
	#draw_stars(old_stars)
	draw_stars(stars,rot)
	#old_stars = copy_stars(stars)
	knot.Draw(Vector(0,0,-50))
	"""c = QuadCube(10)
	c.Draw(Vector(0,-0,-40))
	s = Letter("s")
	s.Draw(Vector(0,50,20))
	t = Letter("t")
	t.Draw(Vector(13,50,20))
	e = Letter("e")
	e.Draw(Vector(26,50,20))
	p = Letter("p")
	p.Draw(Vector(39,50,20))
	h = Letter("h")
	h.Draw(Vector(53,50,20))
	i = Letter("i")
	i.Draw(Vector(67,50,20))
	heart = Letter("heart")
	heart.Draw(Vector(78,50,20))
	"""
	move_stars(stars)

def setup():
	global screen,stars,tex,knot
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	screen = pygame.display.set_mode((1024,768), 0, 32)
	screen.fill((0, 0, 0))
	pygame.display.flip()
	running = True
	#v1 = Vector();
	#v2 = Vector(1,0,0);
	#vc = v1.VecAngle(v2)
	#vc.Print()
	generate_starfield(stars)
	tex = pygame.image.load(os.path.join("game art", "breakout_bg.png"))
	knot = TrefoilKnot(10)

	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
		clock.tick(60)
		tick()
		pygame.display.update()
	pygame.quit()

setup()
