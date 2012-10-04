#!/usr/bin/env python
import os
import pygame
import random
import math
from pygame.locals import *
import os.path, sys
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time

"""
Regolith and baserock layers, the looseness of sediment, contributing area, slope angle, and variable rainfall patterns. 
float contributingArea (CELL *cell)
cell->water = rainfall + contributingArea (all upstream neigbor cells);

return cell->water;


Generally, water will carry sediment downstream until it can''t go any further (i.e. it will deposit in a lake, ocean, crater, etc.). 
"""				

screen = None

iterations = 8 # 2 minimum

waterlevel = 0.1
mountainlevel = 0.57

def createfloatmap(base):
	global iterations
	max = pow(2,iterations)
	floatmap = [[base for x in range(max+1)] for y in range(max+1)]
	return(floatmap)

def diamond(x,y,size,floatmap):
	tl = floatmap[x-size][y-size]
	tr = floatmap[x+size][y-size]
	bl = floatmap[x-size][y+size]
	br = floatmap[x+size][y+size]
	h = (tl+tr+bl+br)/4.0
	return(h)

def square(x,y,size,floatmap):
	global iterations
	pow_max = pow(2,iterations) # 4
	if(x-size <= 0):
		#tl_x = pow_max
		tl_x = pow_max - size
	else:
		tl_x = x-size

	if(x+size >= pow_max):
		#tr_x = 0
		tr_x = 0 + size
	else:
		tr_x = x+size

	if(y-size <= 0):
		#bl_y = pow_max
		bl_y = pow_max - size
	else:
		bl_y = y-size

	if(y+size >= pow_max):
		#br_y = 0
		br_y = 0+size
	else:
		br_y = y+size

	tl = floatmap[tl_x][y]
	tr = floatmap[tr_x][y]
	bl = floatmap[x][bl_y]
	br = floatmap[x][br_y]
	h = (tl+tr+bl+br)/4.0
	return(h)

def clamp(f,min,max):
	if(f<min):
		f = min
	if(f>max):
		f = max
	return(f)

def generate_detail(level,height,floatmap):
	global iterations
	pow_max = pow(2,iterations) # 4 4 
	pow_size = pow(2,iterations-level) # 4 2 
	pow_num = int(pow_max / pow_size) # 1 2
	pow_half_size = int(pow_size / 2)
	x =  pow_half_size
	y = pow_half_size
	for u in range(pow_num):
		x = pow_half_size
		for v in range(pow_num):
			if(pos2height(x,y,floatmap) == -1.0):
				h = diamond(x,y,pow_half_size,floatmap)
				#h = clamp(h + random.uniform(-height,height),0.0,1.0)
				h = clamp(h + random.gauss(0.0,height),0.0,1.0)
				floatmap[x][y] = h

			if(pos2height(x-pow_half_size,y,floatmap) == -1.0):
				h = square(x-pow_half_size,y,pow_half_size,floatmap)
				h = clamp(h + random.gauss(0.0,height),0.0,1.0)
				#h = clamp(h + random.uniform(-height,height),0.0,1.0)
				floatmap[x-pow_half_size][y] = h
				#if(u == 0):
				#	floatmap[x][pow_max] = h
				if(v == 0):
					floatmap[pow_max][y] = h
			
			if(pos2height(x,y-pow_half_size,floatmap) == -1.0):
				h = square(x,y-pow_half_size,pow_half_size,floatmap)
				h = clamp(h + random.gauss(0.0,height),0.0,1.0)
				#h = clamp(h + random.uniform(-height,height),0.0,1.0)
				floatmap[x][y-pow_half_size] = h
				if(u == 0):
					floatmap[x][pow_max] = h
				#if(u == 0):
				#	floatmap[pow_max][y] = h
			"""
			if(pos2height(x+pow_half_size,y,floatmap) == 0.0):
				h = square(x+pow_half_size,y,pow_half_size,floatmap)
				h = clamp(h + random.uniform(-height,height),0.0,1.0)
				floatmap[x+pow_half_size][y] = h
			
			if(pos2height(x,y+pow_half_size,floatmap) == 0.0):
				h = square(x,y+pow_half_size,pow_half_size,floatmap)
				h = clamp(h + random.uniform(-height,height),0.0,1.0)
				floatmap[x][y+pow_half_size] = h
			
			if(v == pow_num-1):
				if(pos2height(x+pow_half_size,y,floatmap) == 0.0):
					h = square(x+pow_half_size,y,pow_half_size,floatmap)
					h = clamp(h + random.uniform(-height,height),0.0,1.0)
					floatmap[x+pow_half_size][y] = h
			if(u == pow_num-1):
				if(pos2height(x,y+pow_half_size,floatmap) == 0.0):
					h = square(x,y+pow_half_size,pow_half_size,floatmap)
					h = clamp(h + random.uniform(-height,height),0.0,1.0)
					floatmap[x][y+pow_half_size] = h
			"""
			x += pow_size
		y += pow_size
	
	if(level + 1 < iterations):
		generate_detail(level+1,height/2.3,floatmap)

def generate_map(height,iterations):
	floatmap = createfloatmap(-1.0)
	powit = pow(2,iterations)
	#floatmap[0][0]  = random.uniform(0.0,height)
	#floatmap[powit][0]  = random.uniform(0.0,height)
	#floatmap[powit][powit]  = random.uniform(0.0,height)
	#floatmap[0][powit] = random.uniform(0.0,height)

	s = random.uniform(0.0,height)
	s = 0.0
	floatmap[0][0]  = s
	floatmap[powit][0]  = s
	floatmap[powit][powit]  = s
	floatmap[0][powit] = s

	pow_size = pow(2,iterations-1) 
	for i in range(random.randint(0,3)):
		x = random.randint(0,powit/pow_size)*pow_size
		y = random.randint(0,powit/pow_size)*pow_size
		floatmap[x][y]  = random.uniform(0.15,0.25)
	
	for x in range(powit+1):
		floatmap[x][0]  = s
	for y in range(powit+1):
		floatmap[powit][y]  = s
	for y in range(powit+1):
		floatmap[0][y]  = s
	for x in range(powit+1):
		floatmap[x][powit] = s

	#floatmap[0][0]  = random.uniform(height/2,height)
	#floatmap[powit][0]  = random.uniform(height/2,height)
	#floatmap[powit][powit]  = random.uniform(height/2,height)
	#floatmap[0][powit] = random.uniform(height/2,height)

	#floatmap[0][0]  = 1.0
	#floatmap[powit][0]  = 1.0
	#floatmap[powit][powit]  = 1.0
	#floatmap[0][powit] = 1.0
	#print("==start configuration==")
	#print(floatmap)
	#print("==start configuration==")
	generate_detail(0,1.0,floatmap)#height
	#print("==end configuration==")
	#print(floatmap)
	#print("==end configuration==")
	return(floatmap)
	
def pos2height(x,y,floatmap):
	return(floatmap[x][y])

def setheight(x,y,height,floatmap):
	if(height >= 0.0 and height <= 1.0):
		floatmap[x][y] = height

def floatmap2surface(floatmap,r,g,b,a):
	global iterations
	max = pow(2,iterations)
	s = pygame.Surface((max+1,max+1),flags = SRCALPHA)
	for x in range(max+1):
		for y in range(max+1):
			#s.set_at((x,y),(int(floatmap[x][y]*255),int(floatmap[x][y]*255),int(floatmap[x][y]*255)))
			s.set_at((x,y),pygame.Color(int(floatmap[x][y]*r),int(floatmap[x][y]*g),int(floatmap[x][y]*b),a))
	return(s)

def watermap2surface(floatmap,r,g,b,a):
	global iterations
	max = pow(2,iterations)
	s = pygame.Surface((max+1,max+1),flags = SRCALPHA)
	for x in range(max+1):
		for y in range(max+1):
			#s.set_at((x,y),(int(floatmap[x][y]*255),int(floatmap[x][y]*255),int(floatmap[x][y]*255)))
			s.set_at((x,y),pygame.Color(int(floatmap[x][y]*r),int(floatmap[x][y]*g),int(floatmap[x][y]*b),int(floatmap[x][y]*a)))
	return(s)

def updatefloatmap(floatmap,newfloatmap,unchanged_value):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
			if(newfloatmap[x][y] != unchanged_value):
				floatmap[x][y] = (floatmap[x][y]*3 + newfloatmap[x][y]*1.0)/4.0
				
def combinefloatmaps(a,b,n,aa,ba):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				n[x][y] = (a[x][y]*aa + b[x][y]*ba)

def invertfloatmap(floatmap):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				floatmap[x][y] = 1.0-floatmap[x][y]

def invertedfloatmap(floatmap):
	global iterations
	max = pow(2,iterations)
	r = createfloatmap(0.0)
	for x in range(max+1):
		for y in range(max+1):
				r[x][y] = 1.0-floatmap[x][y]
	return(r)

def levelfloatmap(floatmap,seamap,level):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				if(floatmap[x][y] < level):
					floatmap[x][y] = level
					seamap[x][y] = 1.0

def levelnormalmap(floatmap,normalmap,level):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				if(floatmap[x][y] < level):
					#floatmap[x][y] = level
					normalmap[x][y] = (0.0,0.0,1.0)

def mountainmap(floatmap,mountainmap,level):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				if(floatmap[x][y] > level):
					mountainmap[x][y] = level

def beachmap(floatmap,beachmap,normalmap,level,height):
	global iterations
	max = pow(2,iterations)
	sun_dir = (-1.0,-1.0,-1.0)
	view_dir = (0.0,0.0,-1.0)
	for x in range(max+1):
		for y in range(max+1):
				if(floatmap[x][y] > level and floatmap[x][y] < level+height):
					sn = Dot(sun_dir,normalmap[x][y])/2.0
					vn = Dot(view_dir,normalmap[x][y])/2.0
					vn = (vn + sn) /2.0
					#vn = sn
					#s.set_at((x,y),pygame.Color(int(127.0*vn+128),int(127.0*vn+128),int(127.0*vn+128),int(127.0*vn+128)))
					beachmap[x][y] = 0.5 * vn + 0.5 

def floatmap2green(floatmap,normalmap,a):
	global iterations
	max = pow(2,iterations)
	sun_dir = (-1.0,-1.0,-1.0)
	view_dir = (0.0,0.0,-1.0)
	s = pygame.Surface((max+1,max+1),flags = SRCALPHA)
	for x in range(max+1):
		for y in range(max+1):
			#s.set_at((x,y),(int(floatmap[x][y]*255),int(floatmap[x][y]*255),int(floatmap[x][y]*255)))
			sn = Dot(sun_dir,normalmap[x][y])/2.0
			vn = Dot(view_dir,normalmap[x][y])/2.0
			vn = (vn + sn) /2.0
			#vn = sn
			g = 1.0-(0.5 * vn + 0.5) 
			r = 1.0-(0.5 * vn + 0.5) 
			b = 1.0-(0.5 * vn + 0.5) 
			#print(g)
			#s.set_at((x,y),pygame.Color(int(floatmap[x][y]*r),int(floatmap[x][y]*g),int(floatmap[x][y]*b),a))
			s.set_at((x,y),pygame.Color(int(r*64.0),int(g*200.0),int(b*64.0),a))
			#s.set_at((x,y),pygame.Color(0,int(g*255.0),0,a))
	return(s)

def Cross(a,b):
	return(( (a[1]*b[2]) - (a[2]*b[1]), (a[2]*b[0]) - (a[0]*b[2]),(a[0]*b[1]) - (a[1]*b[0]) ))

def Add2(a,b):
	return( (a[0] + b[0], a[1] + b[1],a[2] + b[2]) )
	
def Add4(a,b,c,d):
	return( (a[0] + b[0]  + c[0] + d[0] , a[1] + b[1] + c[1] + d[1], -(a[2] + b[2] + c[2] + d[2]) ) )

def Avg(a,b,c,d):
	return( ( (a[0] + b[0]  + c[0] + d[0])/4.0 , (a[1] + b[1] + c[1] + d[1])/4.0, (a[2] + b[2] + c[2] + d[2])/4.0 ) )
	
def Sub(a,b):
	return( (a[0] - b[0], a[1] - b[1], a[2] - b[2]) )
	
def GetLen(a):
	return(math.sqrt((a[0]*a[0]) + (a[1]*a[1]) + (a[2]*a[2])))

def Normalize(a):
	len = GetLen(a)
	if(len == 0.0):
		return((0.0,0.0,0.0))
	return((a[0] / len,a[1] / len,a[2] / len))
	
def pos2height_wrap(x,y,floatmap):
	global iterations
	max = pow(2,iterations)
	if(x<0):
		x = max+1-x
	if(y<0):
		y = max+1-y
	if(x>max):
		x = x-max
	if(y>max):
		y = y-max
	return(floatmap[x][y])

def TriangleNormal(t):
	tu = Sub(t[1],t[0])
	tv = Sub(t[2],t[0])
	tn = Normalize(Cross(tu,tv))
	return(tn)
	
def normalmap(floatmap,normalmap,factor):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
			m = (x+0.0,y+0.0,pos2height_wrap(x,y,floatmap)*max*factor)
			a = (x+1.0,y+0.0,pos2height_wrap(x+1,y,floatmap)*max*factor)
			b = (x+0.0,y-1.0,pos2height_wrap(x,y-1,floatmap)*max*factor)
			c = (x-1.0,y+0.0,pos2height_wrap(x-1,y,floatmap)*max*factor)
			d = (x+0.0,y+1.0,pos2height_wrap(x,y+1,floatmap)*max*factor)
			t1 = (m,c,b)
			t2 = (m,b,a)
			t3 = (m,a,d)
			t4 = (m,d,c)
			t1n = TriangleNormal(t1)
			t2n = TriangleNormal(t2)
			t3n = TriangleNormal(t3)
			t4n = TriangleNormal(t4)
			normalmap[x][y] = Normalize( Avg( t1n,t2n,t3n,t4n ) )
	
def Dot(a,b):
	return( (a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2]))

def normalmap2surface(normalmap):
	global iterations
	max = pow(2,iterations)
	s = pygame.Surface((max+1,max+1),flags = SRCALPHA)
	for x in range(max+1):
		for y in range(max+1):
			#print(normalmap[x][y])
			sun_dir = (-0.50,-1.0,-1.0)
			view_dir = (0.0,0.0,-1.0)
			#sn = Dot(sun_dir,Normalize(Add2(normalmap[x][y],(x,y,0.0))))
			#sn = Dot(sun_dir,Add2(normalmap[x][y],(x,y,0.0)))
			sn = Dot(sun_dir,normalmap[x][y])/2.0
			vn = Dot(view_dir,normalmap[x][y])/2.0
			vn = (vn + sn) /2.0
			#vn = sn
			#print(vn,sn)
			#print(127.0*vn+128)
			#vn = clamp(sn+1.0/2.0,0.0,1.0)
			#
			#if(vn>0.0):
			#	print(vn)
			s.set_at((x,y),pygame.Color(int(127.0*vn+128),int(127.0*vn+128),int(127.0*vn+128),int(127.0*vn+128)))
			#s.set_at((x,y),pygame.Color(int(127.0*vn+128),int(127.0*vn+128),int(127.0*vn+128),int(255.0)))
			#s.set_at((x,y),pygame.Color(int(vn*255.0),int(vn*255.0),int(vn*255.0),int(255.0)))
			#s.set_at((x,y),pygame.Color(int((normalmap[x][y][0]+1.0)/2.0*255.0),int((normalmap[x][y][1]+1.0)/2.0*255.0),int((normalmap[x][y][2]+1.0)/2.0*255.0),255))
			#s.set_at((x,y),pygame.Color(int((normalmap[x][y][0]*127.0)+128.0),int((normalmap[x][y][1]*127.0)+128.0),int((normalmap[x][y][2]*127.0)+128.0),255))
	return(s)
					
def decwatermap(watermap,amount):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
				watermap[x][y] = clamp(watermap[x][y]-amount,0.0,1.0)
				
def Average(x,y,floatmap):
	positions = [ (0,0) , (-1,-1) , (-1,0) , (-1,1) , (0,-1) , (0,1) , (1,-1) , (1,0) , (1,1) ]
	for i in positions:
		h = pos2height_wrap(x+i[0],y+i[1],floatmap)
	h = h / 9.0
	return(h)

def Smooth(floatmap):
	global iterations
	max = pow(2,iterations)
	for x in range(max+1):
		for y in range(max+1):
			Average(x,y,floatmap)
	
def line(s,e,action_at_sample_point):

	pass

def shadowmap(floatmap,shadowmap):
	global iterations
	max = pow(2,iterations)
	factor = 1.5
	print("calculating shadowmap")
	for x in range(max+1):
		for y in range(max+1):
			c = (x+0.0,y+0.0,pos2height_wrap(x,y,floatmap)*max*factor)
			sun_pos = (-2500.0,-5000.0,50000.0)
			light_dir = Normalize(Sub(sun_pos,c))
			shadowmap[x][y] = 1.0
			while(int(c[0]) > 0 and int(c[1]) > 0 and int(c[0])<max+1 and int(c[1]) <max+1):
				c = Add2(c,light_dir)
				sx = int(c[0])
				sy = int(c[1])
				th = pos2height(sx,sy,floatmap)*max*factor
				if(c[2] <= th):
					shadowmap[x][y] = 0.8
					break
	print("calculating shadowmap done")

def FindDeepestNeighbour(x,y,floatmap):
	positions = [ (-1,-1) , (-1,0) , (-1,1) , (0,-1) , (0,1) , (1,-1) , (1,0) , (1,1) ]
	random.shuffle(positions)
	#print(positions)
	h = pos2height(x,y,floatmap)
	deepest_h = 0.0
	deepest_pos = (0,0)
	for i in positions:
		if(floatmap[x+i[0]][y+i[1]] < h and (h-floatmap[x+i[0]][y+i[1]]) > deepest_h):
			deepest_h = h-floatmap[x+i[0]][y+i[1]]	
			deepest_pos = i
			if(random.uniform(0.0,1.0)>0.5):
				return(deepest_pos)
	return(deepest_pos)

def erode(x,y,scale,amount,floatmap,normalmap,watermap):
	global iterations,waterlevel
	view_dir = (0.0,0.0,-1.0)
	max = pow(2,iterations)
	if( (x<0) or (y<0) or (y>(max-2)) or (x>(max-2))):
		return
	#if(newfloatmap[x][y] != -1.0):
	#	return
	power = 0.00515
	h_old = pos2height(x,y,floatmap)
	n_old = normalmap[x][y]
	if(h_old <=  waterlevel-0.3):
		return
	n = FindDeepestNeighbour(x,y,floatmap)
	if(n != (0,0)):
		#print("found neighbour at:",n)
		h_new = pos2height(x+n[0],y+n[1],floatmap)
		n_new = normalmap[x+n[0]][y+n[1]]
		vn_old = Dot(view_dir,n_old)/2.0
		#print(n_new,h_new)
		vn_new = Dot(view_dir,n_new)/2.0
		vn = (vn_old + vn_new) /2.0
		amount = 0.5 * vn + 0.5 

		d = random.uniform(0.0,scale * amount)
		if(h_new <=  waterlevel-0.3):
			return
		
		#if(random.choice((0,1)) == 0):
		#	return
			#a = amount * 1.1
		#else:
		#a = amount * 0.6
		a = amount * vn
		power = 0.5 * (1.0-vn)
		#power = a
		#if(power < 0.5):
		#	power = 0.5
		
		if(h_new > waterlevel):
			erode(x+n[0],y+n[1],scale * 0.5,a,floatmap,normalmap,watermap)
		
		nnh = (h_old + (1.0-power)*(h_new-h_old)) 
		nh = (h_old + power*(h_new-h_old))
		setheight(x+n[0],y+n[1],nnh,floatmap)
		setheight(x,y,nh,floatmap)
		watermap[x+n[0]][y+n[1]] = clamp(watermap[x+n[0]][y+n[1]]+0.01,0.0,1.0)
		watermap[x][y] = clamp(watermap[x][y]-0.01,0.0,1.0)
		
	else:
		#h = h_old - d 
		#if(h>=0.0):
		#	setheight(x,y,h,floatmap)
		#else:
		#	h_old = pos2height(x,y,floatmap)
		#	d = random.uniform(0.0,scale * amount)
		#	#h = h_old + d 
		#	h = h_old + amount*scale
		#	if(h<=1.0):
		#		setheight(x,y,h,floatmap)
		watermap[x][y] = clamp(watermap[x][y]+0.02,0.0,1.0)
		
def tick():pass

def setup():
	global screen,iterations
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	mixer.init()
#	screen = pygame.display.set_mode((1024,768), 0, 32)
	max = pow(2,iterations)
	screen = pygame.display.set_mode((1100,1100), 0, 32)
	screen.fill((120, 100, 80))
	pygame.display.flip ()
	#pygame.init()
	button_down = False
	running = True
	offset_x = 0
	offset_y = 0
	print("generating map")
	floatmap = generate_map(0.0,iterations)
	hmap = floatmap2surface(floatmap,255,255,255,255)
	pygame.image.save(hmap, "original_map.png")
	seamap = createfloatmap(0.0)
	beach = createfloatmap(0.0)
	normal = createfloatmap(0.0)
	shadow = createfloatmap(0.0)
	mountains = createfloatmap(0.0)
	shadowmap(floatmap,shadow)
	#normalmap(floatmap,normal)
	#levelfloatmap(floatmap,seamap,waterlevel-0.3)
	normalmap(floatmap,normal,1.5)
	levelfloatmap(floatmap,seamap,waterlevel)
	levelnormalmap(floatmap,normal,waterlevel-0.3)
	mountainmap(floatmap,mountains,mountainlevel)
	beachmap(floatmap,beach,normal,waterlevel,0.005)
	smap = floatmap2surface(seamap,0,0,255,255)
	bmap = floatmap2surface(beach,255,200,51,128)
	mmap = floatmap2surface(mountains,255,255,255,128)
	shmap = floatmap2surface(shadow,255,255,255,128)
	nmap = normalmap2surface(normal)
	watermap = createfloatmap(0.0)
	combmap = createfloatmap(0.0)
	print("generating done")
	screen.blit(hmap,(0,0))    	
	screen.blit(shmap,(max,0))    	
	screen.blit(bmap,(0,max))    	
	screen.blit(nmap,(max,max))    	
	pygame.image.save(smap, "sea_map.png")
	pygame.image.save(bmap, "beach_map.png")
	pygame.image.save(mmap, "mountain_map.png")
	pygame.image.save(nmap, "normal_map.png")
	pygame.image.save(shmap, "shadow_map.png")
	
	old_pos = pygame.mouse.get_pos()
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
			if(e.type == pygame.MOUSEBUTTONDOWN):
				button_down = True
			if(e.type == pygame.MOUSEBUTTONUP):
				button_down = False

		#screen.blit(smap,(0,0))    	
		pygame.display.update()
		tick()
		clock.tick(50)
		button_down = True
		if(button_down):
			pos = pygame.mouse.get_pos()
			rel_x = pos[0] - old_pos[0]
			rel_y = pos[1] - old_pos[1]
			offset_x += rel_x
			offset_y += rel_y
			old_pos = pos;
			"""
			print("generating map")
			floatmap = generate_map(1.0)
			print("generating done")
			smap = floatmap2surface(floatmap)
			screen.blit(smap,(0,0))    	
			screen.blit(smap,(511,0))    	
			screen.blit(smap,(0,511))    	
			screen.blit(smap,(511,511))    	
			"""
			#print("generating map")
			#map = generate_map(1.0)
			#render_map(map,offset_x,offset_y,255)
			#print("generating done")
			#print("eroding map")
			
			#newfloatmap = createfloatmap(-1.0)
				#erode(random.randint(0,pow(2,iterations)-1),random.randint(0,pow(2,iterations)-1),random.uniform(0.01,0.02),random.uniform(0.1,0.8),floatmap,watermap)
				#updatefloatmap(floatmap,newfloatmap,-1.0)
			#erode(pos[0],pos[1],floatmap,newfloatmap)
			#print("eroding done")
			imap = invertedfloatmap(watermap)
			combinefloatmaps(floatmap,watermap,combmap,0.8,0.2)
			#combinefloatmaps(floatmap,imap,combmap,0.5,0.5)

			hmap = floatmap2surface(floatmap,255,255,255,255)
			hgmap = floatmap2green(floatmap,normal,255)
			#hmap = floatmap2surface(floatmap,255,255,255,255)
			pygame.image.save(hmap, "erosion_map.png")
			screen.blit(hmap,(0,max))    	
			#hmap = floatmap2surface(floatmap,0,255,0,255)
			hmap = floatmap2surface(combmap,0,255,0,255)
			pygame.image.save(hmap, "green_map.png")
			wmap = watermap2surface(watermap,0,0,255,128)
			#hmap.blit(wmap,(0,0),special_flags=BLEND_MULT)    	
			hmap.blit(hgmap,(0,0),special_flags=BLEND_ADD)    	
			hmap.blit(smap,(0,0),special_flags=BLEND_ADD)    	
			#hmap.blit(wmap,(0,0),special_flags=BLEND_ADD)    	
			#hmap.blit(wmap,(0,0),special_flags=BLEND_MULT)    	
			hmap.blit(bmap,(0,0),special_flags=BLEND_ADD)    	
			hmap.blit(mmap,(0,0),special_flags=BLEND_ADD)    	
			#hmap.blit(nmap,(0,0),special_flags=BLEND_ADD)    	
			hmap.blit(nmap,(0,0),special_flags=BLEND_MULT)    	
			hmap.blit(shmap,(0,0),special_flags=BLEND_MULT)    	
			#hmap.blit(nmap,(0,0),special_flags=BLEND_RGBA_ADD)    	


			cmap = floatmap2surface(combmap,255,255,255,255)
			pygame.image.save(cmap, "combine_map.png")
			screen.blit(cmap,(max,0))    	
			#hmap.blit(cmap,(0,0),special_flags=BLEND_ADD)    	
			pygame.image.save(hmap, "combi_map.png")
			#hmap.blit(wmap,(0,0))    	
			screen.blit(hmap,(0,0))    	
			wmap = floatmap2surface(watermap,255,255,255,255)
			pygame.image.save(wmap, "water_map.png")
			screen.blit(wmap,(max,max))    	
			print("eroding")
			for i in range(1):
				for x in range(max):			
					for y in range(max):			
						erode(x,y,random.uniform(0.1,0.6),random.uniform(0.2,0.6),floatmap,normal,watermap)
			Smooth(floatmap)
			#normal = createfloatmap(0.0)
			normalmap(floatmap,normal,1.5)
			nmap = normalmap2surface(normal)
			decwatermap(watermap,0.00001)
			Smooth(watermap)
			Smooth(watermap)
			Smooth(watermap)
			Smooth(watermap)
			print("eroding done")
			#floatmap = newfloatmap
			#render_map(map,offset_x,offset_y,255)
			#h = pos2height(pos[0],pos[1],map)
			#print(h)
			#setheight(pos[0],pos[1],0.1122,map)
			#h = pos2height(pos[0],pos[1],map)
			#print(h)
	pygame.quit()

setup()