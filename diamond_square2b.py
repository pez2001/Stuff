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

iterations =  8 # 2 minimum

def generate_detail(level,map):
	global iterations
	pow_max = pow(2,iterations) # 4 4 
	pow_size = pow(2,iterations-level) # 4 2 
	
	#diamond step
	for i in range(int(pow_max / pow_size)): # 0 , 0 1
		for d in range(int(pow_max / pow_size)): # 0 , 0 1
			h = 0
			x = 0
			y = 0
			print("diamond")
			for u in range(2):
				for v in range(2):
					tx = int(i * pow_size + u*pow_size)
					ty = int(d * pow_size + v*pow_size)
					print(tx," ",ty)
					h += map[tx][ty]
					y += pow_size
		
				x += pow_size
			h = h / 4 + random.uniform(0.0,100.0/(level +1))
			map[int(i*pow_size+pow_size/2)][int(d*pow_size+pow_size/2)] = h
		
	#square step
	#for i in range(int(pow_max / (pow_size/2))): # 2 , 
	
	if(iterations == level + 1):
		return(map)
	else:
		return(generate_detail(level+1,map))
	

def generate_map2():
	map = [[0 for x in range(pow(2,iterations)+1)] for y in range(pow(2,iterations)+1)]
	map[0][0]  = random.uniform(0.0,100.0)
	powit = pow(2,iterations)
	map[powit][0]  = random.uniform(0.0,100.0)
	map[powit][powit]  = random.uniform(0.0,100.0)
	map[0][powit] = random.uniform(0.0,100.0)
	print("==start configuration==")
	render_map(map,0,0)
	print("==start configuration==")
	return(generate_detail(0,map))

	
def generate_level(level,map,height):
	global iterations
	#create a 3x3 array from the 2x2 array
	#mid = (map[0][0]+map[1][0]+map[0][1]+map[1][1])/4.0 + random.uniform(-height/(level),height/(level))
	mid = (map[0][0]+map[1][0]+map[0][1]+map[1][1] )/4.0+ random.uniform(-height/(level),height/(level))
	if(mid > 1.0):
		mid = 1.0
	if(mid < 0.0):
		mid = 0.0
	new_map = [[map[0][0],(map[0][0]+map[1][0])/2.0,map[1][0]],[(map[0][0]+map[0][1])/2.0,mid,(map[1][0]+map[1][1])/2.0],[map[0][1],(map[0][1]+map[1][1])/2.0,map[1][1]]]
	#create 2x2 arrays for recursive subdivison
	sub_tl = [[new_map[0][0],new_map[1][0]],[new_map[0][1],new_map[1][1]]]
	sub_tr = [[new_map[1][0],new_map[2][0]],[new_map[1][1],new_map[2][1]]]
	sub_bl = [[new_map[0][1],new_map[1][1]],[new_map[0][2],new_map[1][2]]]
	sub_br = [[new_map[1][1],new_map[2][1]],[new_map[1][2],new_map[2][2]]]
	if(iterations == level ):
		return(new_map)
	#recurse 3x3 sub maps
	sub_tl_map = generate_level(level+1,sub_tl,height)
	sub_tr_map = generate_level(level+1,sub_tr,height)
	sub_bl_map = generate_level(level+1,sub_bl,height)
	sub_br_map = generate_level(level+1,sub_br,height)
	#create array of sub maps
	subs_map = [sub_tl_map,sub_tr_map,sub_bl_map,sub_br_map]
	#create 5x5 array of sub maps
	#subs_map = [[sub_tl_map[0][0],sub_tl_map[1][0],sub_tl_map[2][0],sub_tr_map[1][0],sub_tr_map[2][0]] , [sub_tl_map[0][1],sub_tl_map[1][1],sub_tl_map[2][1],sub_tr_map[1][1],sub_tr_map[2][1]] , [sub_tl_map[0][2],sub_tl_map[1][2],sub_tl_map[2][2],sub_tr_map[1][2],sub_tr_map[2][2]] , [sub_bl_map[0][1],sub_bl_map[1][1],sub_bl_map[2][1],sub_br_map[1][1],sub_br_map[2][1]] , [sub_bl_map[0][2],sub_bl_map[1][2],sub_bl_map[2][2],sub_br_map[1][2],sub_br_map[2][2]] ]
	return(subs_map)	
	
def generate_map(height):
	map = [[random.uniform(0.0,height/2.0),random.uniform(0.0,height/2.0)],[random.uniform(0.0,height/2.0),random.uniform(0.0,height/2.0)]]
#	map = [[random.uniform(0.0,0.3),random.uniform(0.0,0.3)],[random.uniform(0.0,0.3),random.uniform(0.0,0.3)]]
#	map = [[0.0,0.0],[0.0,0.0]]
	return(generate_level(1,map,height))
	
	
def render_quad(level,x,y,map_quad,floatmap):
	global iterations,screen
	if(iterations > level +1):
		render_quad(level+1,x,y,map_quad[0],floatmap)
		render_quad(level+1,x+pow(2,iterations-level-1),y,map_quad[1],floatmap)
		render_quad(level+1,x,y+pow(2,iterations-level-1),map_quad[2],floatmap)
		render_quad(level+1,x+pow(2,iterations-level-1),y+pow(2,iterations-level-1),map_quad[3],floatmap)
		return
	#print(x,y)
	#print(map_quad)
	floatmap[x+0][y+0] = map_quad[0][0]
	floatmap[x+1][y+0] = map_quad[1][0]
	floatmap[x+0][y+1] = map_quad[0][1]
	floatmap[x+1][y+1] = map_quad[1][1]

def createfloatmap(base):
	global iterations
	floatmap = [[base for x in range(pow(2,iterations))] for y in range(pow(2,iterations))]
	return(floatmap)
	
def render_map(map):
	floatmap = createfloatmap(0.0)
	render_quad(0,0,0,map,floatmap)
	return(floatmap)

def floatmap2surface(floatmap):
	global iterations
	s = pygame.Surface((pow(2,iterations),pow(2,iterations)))
	for x in range(pow(2,iterations)):
		for y in range(pow(2,iterations)):
			s.set_at((x,y),(int(floatmap[x][y]*255),int(floatmap[x][y]*255),int(floatmap[x][y]*255)))
	return(s)
	
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
	print("generating map")
	maptree = generate_map(1.0)
	print("generating done")
#	screen = pygame.display.set_mode((1024,768), 0, 32)
	screen = pygame.display.set_mode((640,480), 0, 32)
	screen.fill((120, 100, 80))
	pygame.display.flip ()
	#pygame.init()
	button_down = False
	running = True
	offset_x = 0
	offset_y = 0
	floatmap = render_map(maptree)
	#print(floatmap)
	smap = floatmap2surface(floatmap)
	pygame.image.save(smap, "omap.png")
	
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
		#print("generating map")
			#map = generate_map(1.0)
			#render_map(map,offset_x,offset_y,255)
			#print("generating done")
		print("eroding map")
		for i in range(500):
			newfloatmap = createfloatmap(-1.0)
			erode(random.randint(0,pow(2,iterations)-1),random.randint(0,pow(2,iterations)-1),floatmap,newfloatmap)
			updatefloatmap(floatmap,newfloatmap,-1.0)
			#erode(pos[0],pos[1],floatmap,newfloatmap)
		print("eroding done")
		smap = floatmap2surface(floatmap)
		pygame.image.save(smap, "map.png")
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