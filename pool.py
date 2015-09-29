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

	def __add__(self,value):
		return(Vector(self.x+value.x,self.y+value.y,self.z+value.z))

	def __sub__(self,value):
		return(Vector(self.x-value.x,self.y-value.y,self.z-value.z))
	def __div__(self,value):
		return(Vector(self.x/value,self.y/value,self.z/value))
#		if(type(b).__name__ == "float" or type(b).__name__ == "int"):
#			return(Vector(a.x/b,a.y/b,a.z/b))
#		else:
#		return(Vector(self.x/value.x,self.y/value.y,self.z/value.z))

	
	def __mul__(self,value):
		if(type(value).__name__ == "float" or type(value).__name__ == "int"):
			return(Vector(self.x*value,self.y*value,self.z*value))
		else:
			return(Vector(self.x*value.x,self.y*value.y,self.z*value.z))
		
	def Copy(self):
		return(Vector(self.x,self.y,self.z))		

	
	def Draw2D(self,color):
		global screen
		x = int(self.x)
		y = int(self.y)
		if(x>=0 and x<screen.get_width() and y>=0 and y<screen.get_height()):
			screen.set_at((x,y),color)

	def Draw(self,color):
		global screen
		s = self.Project()
		x = int(s.x)
		y = int(s.y)
		#print(x,y)
		if(x>=0 and x<screen.get_width() and y>=0 and y<screen.get_height()):
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
			fov = 120
			dist = 1
			if(self.z != 0):
				if(self.z > 0.0):
					v = Vector(self.x * fov / (self.z + dist) + screen.get_width()/2,-self.y * fov / (self.z + dist) + screen.get_height()/2,0)
				else:
					v = Vector(-1,-1,0);
			else:
				v = Vector(self.x * fov / (0.1) + screen.get_width()/2,-self.y * fov / (0.1 + dist) + screen.get_height()/2,0)
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

	
stars_num = 30
stars = [None for x in range(stars_num)]
stars_vel = [None for x in range(stars_num)]
stars_mass = [None for x in range(stars_num)]
stars_rad = [None for x in range(stars_num)]
stars_old = [None for x in range(stars_num)]
dim = 2000
dimz = 2000

def generate_starfield(stars):
	global dim,dimz
	for i in range(len(stars)):
		stars[i] = Vector(random.randint(-dim,dim),random.randint(-dim,dim),random.randint(0,dimz))
		stars_old[i] = stars[i].Copy()
	for i in range(len(stars)):
		stars_vel[i] = Vector(random.random(),random.random(),random.random()).Normalize()*0.10
		stars_mass[i] = random.random()*3
		stars_rad[i] = random.random()*2

def draw_stars(stars,angle):
	global screen,dimz
	screen.fill((0, 0, 0))
	for i in range(len(stars)):
		#r = stars[i].RotateZ(angle)
		r = stars[i]
		
		#stars_old[i].Draw2D(pygame.Color(0,0,0,0))
		#stars_old[i] = r.Project()
		#c = int(255.0 * (1.0 - (stars[i].z / dimz)))
		c = int(stars_mass[i]/10)
		if(c<0):
			c = 0
		if(c>255):
			c = 255
		col = pygame.Color(255,c,c,255)
		r.Draw(col)
		rc = r.Project()
		#rc = r.Project()
		zz = r.z	
		if(zz == 0.0):
			zz = 0.1		
		dr = int(stars_rad[i]/(zz*0.001))
		if(dr < 0):
			dr=-dr
		if(dr == 0):
			dr = 1
		dr_c = dr
		if(dr_c > 255):
			dr_c = 255
		ccol = pygame.Color(c,dr_c,255,200)
		if(rc.x-dr >= 0 and rc.x-dr < screen.get_width() and rc.y-dr >= 0 and rc.y < screen.get_height()):
			pygame.draw.circle(screen,ccol,(int(rc.x),int(rc.y)),dr)
		#c = 255
		r2 = r.Project()
		r3 = Vector(r.x,r.y,r.z-(0.5*r.z/r.GetLen())).Project()
		#if(int(r2.x) >= 0 and int(r2.x) < screen.get_width() and int(r2.y) >= 0 and int(r2.y) < screen.get_height()):
		#	if(int(r3.x) >= 0 and int(r3.x) < screen.get_width() and int(r3.y) >= 0 and int(r3.y) < screen.get_height()):
		#		pygame.gfxdraw.line(screen, int(r2.x),int(r2.y),int(r3.x),int(r3.y), col)

#	for i in stars_old:
#		i.Draw(pygame.Color(0,0,0))
#	for i in stars:
#		r = i.RotateZ(angle)
#		c = int(255.0 * (1.0 - (i.z / dimz)))
#		if(c<0):
#			c = 0
#		if(c>255):
#			c = 255
#		if(clear):
#			r.Draw(pygame.Color(0,0,0))
#		else:
#			r.Draw(pygame.Color(c,c,c,c))

def zoom_stars(stars,zoom):
	global dim,dimz
	for i in range(len(stars)):
		stars[i].z -= zoom

w = Vector(0,0,30)
def move_stars(stars):
	global dim,dimz
	for i in range(len(stars)):
		#stars_old[i] = stars[i].Copy
		#stars[i].z -= 0.1
		#stars_vel[i] += (w-stars[i]).Normalize() / Vector((stars[i]-w).GetLen(),(stars[i]-w).GetLen(),(stars[i]-w).GetLen())
		#stars_vel[i] += ((w-stars[i]).Normalize()*0.5) * (0.01 / (stars[i]-w).GetLen())
		#stars[i] += stars_vel[i]
		for b in range(len(stars)):
			if(i != b):
				if(abs((stars[b]-stars[i]).GetLen()) < (stars_rad[b]+stars_rad[i])):
					stars[i].x = (stars[i].x*0.5) + (stars[b].x*0.5) 
					stars[i].y = (stars[i].y*0.5) + (stars[b].y*0.5) 
					stars[i].z = (stars[i].z*0.5) + (stars[b].z*0.5) 
					stars[b].z = random.randint(-dim,dim)
					stars[b].x = random.randint(-dim,dim)
					stars[b].y = random.randint(-dim,dim)
					stars_rad[i] = (stars_rad[i]*0.5) + (stars_rad[b]*0.5)
					stars_vel[i] = (stars_vel[i]*0.5) + (stars_vel[b]*0.5)
					stars_mass[i] = (stars_mass[i]*0.5) + (stars_mass[b]*0.5)
					stars_vel[b] = Vector(random.randint(-dim,dim),random.randint(-dim,dim),random.randint(0,dimz)).Normalize()*0.10
					stars_mass[b] = random.random()*2
					stars_rad[b] = random.random()*2


				#stars_vel[i] += ((stars[b]-stars[i]).Normalize()) * (0.005 / (stars[b]-stars[i]).GetLen())
				stars_vel[i] += ((stars[b]-stars[i]).Normalize()) * (0.05*(stars_mass[b]+stars_mass[i]) / (stars[b]-stars[i]).GetLen() )
		stars_vel[i] *= 0.998
		stars[i] += stars_vel[i]

		#rad = r * math.pi / 180
		#i.x = i.x*math.cos(rad) - i.y*math.sin(rad)
		#iy = i.x*math.sin(rad) + i.y*math.cos(rad)
#		if(stars[i].z <= 0.0):
#			#i.z = random.randint(dimz-100,dimz)
#			stars[i].z = dimz
#			stars[i].x = random.randint(-dim,dim)
#			stars[i].y = random.randint(-dim,dim)
			
		
rot = 0.0

def tick():
	global rot
	rot += 0.7
	#draw_stars(stars_old,rot,True)
	move_stars(stars)
	draw_stars(stars,rot)
	#old_stars = copy_stars(stars)
	#s = Letter("s")
	#s.Draw(Vector(0,0,20))
	#t = Letter("t")
	#t.Draw(Vector(13,0,20))
	#e = Letter("e")
	#e.Draw(Vector(26,0,20))
	#p = Letter("p")
	#p.Draw(Vector(39,0,20))
	#h = Letter("h")
	#h.Draw(Vector(52,0,20))
	#i = Letter("i")
	#i.Draw(Vector(65,0,20))
	#heart = Letter("heart")
	#heart.Draw(Vector(78,0,20))

def setup():
	global screen,stars
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	screen = pygame.display.set_mode((1000,800),  0, 32,)
	#screen = pygame.display.set_mode((0,0),  pygame.FULLSCREEN, 32,)
	#screen = pygame.display.set_mode((1024,768),  pygame.FULLSCREEN, 32,)
	screen.fill((0, 0, 0))
	pygame.display.flip ()
	running = True
	generate_starfield(stars)

	z = 0
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
			if(e.type == pygame.KEYDOWN and e.key == pygame.K_UP):
				z = 1
			if(e.type == pygame.KEYUP and e.key == pygame.K_UP):
				z = 0
			if(e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN):
				z = -1
			if(e.type == pygame.KEYUP and e.key == pygame.K_DOWN):
				z = 0
		zoom_stars(stars,z)
		clock.tick(60)
		tick()
		pygame.display.update()
	pygame.quit()

setup()