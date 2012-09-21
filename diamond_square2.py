#!/usr/bin/env python
import os
import pygame
import random
from pygame.locals import *
import os.path, sys
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time


screen = None

iterations =  9 # 2 minimum

def diamond(x,y,size,floatmap):
	tl = floatmap[x-size][y-size]
	tr = floatmap[x+size][y-size]
	bl = floatmap[x-size][y+size]
	br = floatmap[x+size][y+size]
	h = (tl+tr+bl+br)/4.0
	#print("diamond",h)
	return(h)

def square(x,y,size,floatmap):
	#handle overflow
	global iterations
	pow_max = pow(2,iterations) # 4
	#if(x-size < 0):
	if(x-size <= 0):
		tl_x = pow_max
		#tl_x = pow_max - size
	else:
		tl_x = x-size

	#if(x+size > pow_max):
	if(x+size >= pow_max):
		tr_x = 0
		#tr_x = 0 + size
	else:
		tr_x = x+size

	#if(y-size < 0):
	if(y-size <= 0):
		bl_y = pow_max
		#bl_y = pow_max - size
	else:
		bl_y = y-size

	#if(y+size > pow_max):
	if(y+size >= pow_max):
		br_y = 0
		#br_y = 0+size
	else:
		br_y = y+size

	tl = floatmap[tl_x][y]
	tr = floatmap[tr_x][y]
	bl = floatmap[x][bl_y]
	br = floatmap[x][br_y]
	h = (tl+tr+bl+br)/4.0
	#print("square",h)
	return(h)

def generate_detail(level,height,floatmap):
	global iterations
	pow_max = pow(2,iterations) # 4 4 
	pow_size = pow(2,iterations-level) # 4 2 
	pow_num = int(pow_max / pow_size) # 1 2
	#print("detail",pow_max,pow_size,pow_size/2,pow_num,level+1,iterations)
#		h = h / 4 + random.uniform(0.0,100.0/(level +1))
#		map[int(i*pow_size+pow_size/2)][int(d*pow_size+pow_size/2)] = h
	x =  int(pow_size / 2)
	y = int(pow_size / 2)
	for u in range(pow_num):
		x = int(pow_size / 2)
		for v in range(pow_num):
			h = diamond(x,y,int(pow_size / 2),floatmap)
			h = h + random.uniform(-height,height)
			if(h< 0.0):
				h = 0.0
			if(h > 1.0):
				h = 1.0
			floatmap[x][y] = h

			h = square(x-int(pow_size / 2),y,int(pow_size / 2),floatmap)
			h = h + random.uniform(-height,height)
			if(h< 0.0):
				h = 0.0
			if(h > 1.0):
				h = 1.0
			floatmap[x-int(pow_size / 2)][y] = h
			
			h = square(x,y-int(pow_size / 2),int(pow_size / 2),floatmap)
			h = h + random.uniform(-height,height)
			if(h< 0.0):
				h = 0.0
			if(h > 1.0):
				h = 1.0
			floatmap[x][y-int(pow_size / 2)] = h

			if(v == pow_num-1):
				h = square(x+int(pow_size / 2),y,int(pow_size / 2),floatmap)
				h = h + random.uniform(-height,height)
				if(h< 0.0):
					h = 0.0
				if(h > 1.0):
					h = 1.0
				floatmap[x+int(pow_size / 2)][y] = h
			if(u == pow_num-1):
				h = square(x,y+int(pow_size / 2),int(pow_size / 2),floatmap)
				h = h + random.uniform(-height,height)
				if(h< 0.0):
					h = 0.0
				if(h > 1.0):
					h = 1.0
				floatmap[x][y+int(pow_size / 2)] = h

			x += pow_size
			
			

		y += pow_size
		
			
			
	"""	
	x =  int(pow_max)
	y = int(pow_size / 2)
	for u in range(pow_num):
		h = square(x,y,int(pow_size / 2),floatmap)
		h = h + random.uniform(-height,height)
		if(h< 0.0):
			h = 0.0
		if(h > 1.0):
			h = 1.0
		floatmap[x][y] = h
		y += pow_size

	x =  int(pow_size / 2)
	y = int(pow_max)
	for v in range(pow_num):
		h = square(x,y,int(pow_size / 2),floatmap)
		h = h + random.uniform(-height,height)
		if(h< 0.0):
			h = 0.0
		if(h > 1.0):
			h = 1.0
		floatmap[x][y] = h
		x += pow_size
	"""
	
	
	if(level + 1 < iterations):
		generate_detail(level+1,height/2,floatmap)
	

def createfloatmap(base):
	global iterations
	floatmap = [[base for x in range(pow(2,iterations)+1)] for y in range(pow(2,iterations)+1)]
	return(floatmap)

def floatmap2surface(floatmap):
	global iterations
	s = pygame.Surface((pow(2,iterations),pow(2,iterations)))
	for x in range(pow(2,iterations)):
		for y in range(pow(2,iterations)):
			s.set_at((x,y),(int(floatmap[x][y]*255),int(floatmap[x][y]*255),int(floatmap[x][y]*255)))
	return(s)

def generate_map(height):
	floatmap = createfloatmap(0.0)
	powit = pow(2,iterations)
	#floatmap[0][0]  = random.uniform(0.0,height)
	#floatmap[powit][0]  = random.uniform(0.0,height)
	#floatmap[powit][powit]  = random.uniform(0.0,height)
	#floatmap[0][powit] = random.uniform(0.0,height)

	s = random.uniform(0.0,height)
	floatmap[0][0]  = s
	floatmap[powit][0]  = s
	floatmap[powit][powit]  = s
	floatmap[0][powit] = s

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
	generate_detail(0,height/4,floatmap)
	#print("==end configuration==")
	#print(floatmap)
	#print("==end configuration==")
	return(floatmap)
	
	
def tick():pass
 

def pos2height(x,y,floatmap):
	return(floatmap[x][y])

def setheight(x,y,height,floatmap):
	if(height >= 0.0 and height <= 1.0):
		floatmap[x][y] = height

def updatefloatmap(floatmap,newfloatmap,unchanged_value):
	global iterations
	for x in range(pow(2,iterations)):
		for y in range(pow(2,iterations)):
			if(newfloatmap[x][y] != unchanged_value):
				floatmap[x][y] = newfloatmap[x][y]
				

def erode(x,y,floatmap,newfloatmap):
	global iterations
	max = pow(2,iterations)
	if( (x<0) or (y<0) or (y>(max-2)) or (x>(max-2))):
		return
	if(newfloatmap[x][y] != -1.0):
		return
	h_mm =pos2height(x,y,floatmap)
	if(h_mm-0.1>=0.0):
		setheight(x,y,h_mm-random.uniform(0.0,0.1),newfloatmap)

	h_tl =pos2height(x-1,y-1,floatmap)
	if(h_tl<h_mm and random.choice((0,1)) == 0):
		erode(x-1,y-1,floatmap,newfloatmap)
	h_tm =pos2height(x,y-1,floatmap)
	if(h_tm<h_mm and random.choice((0,1)) == 0):
		erode(x,y-1,floatmap,newfloatmap)
	h_tr =pos2height(x+1,y-1,floatmap)
	if(h_tr<h_mm and random.choice((0,1)) == 0):
		erode(x+1,y-1,floatmap,newfloatmap)
	h_ml =pos2height(x-1,y,floatmap)
	if(h_ml<h_mm and random.choice((0,1)) == 0):
		erode(x-1,y,floatmap,newfloatmap)
	h_mr =pos2height(x+1,y,floatmap)
	if(h_mr<h_mm and random.choice((0,1)) == 0):
		erode(x+1,y,floatmap,newfloatmap)
	h_bl =pos2height(x-1,y+1,floatmap)
	if(h_bl<h_mm and random.choice((0,1)) == 0):
		erode(x-1,y+1,floatmap,newfloatmap)
	h_bm =pos2height(x,y+1,floatmap)
	if(h_bm<h_mm and random.choice((0,1)) == 0):
		erode(x,y+1,floatmap,newfloatmap)
	h_br =pos2height(x+1,y+1,floatmap)
	if(h_br<h_mm and random.choice((0,1)) == 0):
		erode(x+1,y+1,floatmap,newfloatmap)



def setup():
	global screen
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	mixer.init()
#	screen = pygame.display.set_mode((1024,768), 0, 32)
	screen = pygame.display.set_mode((1100,1100), 0, 32)
	screen.fill((120, 100, 80))
	pygame.display.flip ()
	#pygame.init()
	button_down = False
	running = True
	offset_x = 0
	offset_y = 0
	print("generating map")
	floatmap = generate_map(1.0)
	print("generating done")
	smap = floatmap2surface(floatmap)
	screen.blit(smap,(0,0))    	
	screen.blit(smap,(511,0))    	
	screen.blit(smap,(0,511))    	
	screen.blit(smap,(511,511))    	
	pygame.image.save(smap, "omap2.png")
	
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
		print("eroding map")
		for i in range(50):
			newfloatmap = createfloatmap(-1.0)
			erode(random.randint(0,pow(2,iterations)-1),random.randint(0,pow(2,iterations)-1),floatmap,newfloatmap)
			updatefloatmap(floatmap,newfloatmap,-1.0)
			#erode(pos[0],pos[1],floatmap,newfloatmap)
		print("eroding done")
		smap = floatmap2surface(floatmap)
		pygame.image.save(smap, "dmap.png")
		screen.blit(smap,(0,0))    	
			#floatmap = newfloatmap
			#render_map(map,offset_x,offset_y,255)
			#h = pos2height(pos[0],pos[1],map)
			#print(h)
			#setheight(pos[0],pos[1],0.1122,map)
			#h = pos2height(pos[0],pos[1],map)
			#print(h)
	pygame.quit()

setup()