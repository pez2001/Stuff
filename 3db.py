#!/usr/bin/env python
import os
import pygame
import pygame.gfxdraw
import random
import math
"""globals"""
image_dir = "./images"
screen = None

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
#		for v in self.vertices:
#				d = v + offset
#				d.Draw(pygame.Color("white"))
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


					
class Face():
	def __init__(self,p1,p2,p3):
		self.vertices = [p1,p2,p3]

	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(Face(self.vertices[0]*b,self.vertices[1]*b,self.vertices[2]*b))

class Mesh():
	def __init__(self,*faces):
		self.faces = faces
		
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



class Cube(Mesh):
	def __init__(self,size):
		#size is a float
		self.faces = []
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)
		self.faces.append(Face(Vector(0,0,0),Vector(0,0,0),Vector(0,0,0))*size)

		

		


class Vector():
	def __init__(self, x = 0.0,y = 0.0,z = 0.0):
			self.x = x
			self.y = y
			self.z = z

	def __add__(a,b):
		return(Vector(a.x+b.x,a.y+b.y,a.z+b.z))

	def __sub__(a,b):
		return(Vector(a.x-b.x,a.y-b.y,a.z-b.z))

	def __div__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(Vector(a.x/b,a.y/b,a.z/b))
		else:
			return(Vector(a.x/b.x,a.y/b.y,a.z/b.z))

	
	def __mul__(a,b):
		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
			return(Vector(a.x*b,a.y*b,a.z*b))
		else:
			return(Vector(a.x*b.x,a.y*b.y,a.z*b.z))
		
	def Copy(self):
		return(Vector(self.x,self.y,self.z))		

	def Draw(self,color):
		global screen
		s = self.Project()
		x = int(s.x)
		y = int(s.y)
		#print(x,y)
		if(x>0 and x<screen.get_width() and y>0 and y<screen.get_height()):
			screen.set_at((x,y),color)
	def GetLen(self):
		return(math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z))

	def Normalize(self):
		len = self.GetLen()
		if(len == 0):
			return
		return(Vector(self.x / len,self.y / len,self.z / len))	
		
	def Project(self):
			global screen
			fov = 100
			dist = 40
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

	
stars_num = 3000
stars = [None for x in range(stars_num)]
stars_vel = [None for x in range(stars_num)]
stars_old = [None for x in range(stars_num)]
dim = 2000
dimz = 1000

def generate_starfield(stars):
	global dim,dimz
	for i in range(len(stars)):
		stars[i] = Vector(random.randint(-dim,dim),random.randint(-dim,dim),random.randint(0,dimz))
		stars_old[i] = stars[i].Copy()
	for i in range(len(stars)):
		stars_vel[i] = Vector(random.randint(-dim,dim),random.randint(-dim,dim),random.randint(0,dimz)).Normalize()*0.10

def draw_stars(stars,angle,clear = False):
	global screen,dimz
	screen.fill((0, 0, 0))
	for i in stars_old:
		r = i.RotateZ(angle-0.3)
		r.Draw(pygame.Color(0,0,0))
	for i in stars:
		r = i.RotateZ(angle)
		c = int(255.0 * (1.0 - (i.z / dimz)))
		if(c<0):
			c = 0
		if(c>255):
			c = 255
		if(clear):
			r.Draw(pygame.Color(0,0,0))
		else:
			r.Draw(pygame.Color(c,c,c,c))

def move_stars(stars):
	global dim,dimz
	for i in range(len(stars)):
		#stars_old[i] = stars[i].Copy
#		stars[i].z -= 1.5
		stars[i] += stars_vel[i]
		#rad = r * math.pi / 180
		#i.x = i.x*math.cos(rad) - i.y*math.sin(rad)
		#iy = i.x*math.sin(rad) + i.y*math.cos(rad)
		if(stars[i].z <= -40.0):
			#i.z = random.randint(dimz-100,dimz)
			stars[i].z = dimz
			stars[i].x = random.randint(-dim,dim)
			stars[i].y = random.randint(-dim,dim)
			
		
rot = 0.0

def tick():
	global rot
	rot += 0.3
	#draw_stars(stars_old,rot,True)
	move_stars(stars)
	draw_stars(stars,rot)
	#old_stars = copy_stars(stars)
	s = Letter("s")
	s.Draw(Vector(0,0,20))
	t = Letter("t")
	t.Draw(Vector(13,0,20))
	e = Letter("e")
	e.Draw(Vector(26,0,20))
	p = Letter("p")
	p.Draw(Vector(39,0,20))
	h = Letter("h")
	h.Draw(Vector(52,0,20))
	i = Letter("i")
	i.Draw(Vector(65,0,20))
	heart = Letter("heart")
	heart.Draw(Vector(78,0,20))

def setup():
	global screen,stars
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	screen = pygame.display.set_mode((1024,768), 0, 32)
	screen.fill((0, 0, 0))
	pygame.display.flip ()
	running = True
	generate_starfield(stars)
	
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
		clock.tick(60)
		tick()
		pygame.display.update()
	pygame.quit()

setup()