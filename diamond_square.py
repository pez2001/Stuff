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

iterations =  7 # 2 minimum

def diamond():
	pass
def square():
	pass

"""def generate_detail(level,map):
	global iterations
	
	powl = pow(2,level) # 0 2 
	powit = pow(2,iterations-level) # 4 2 
	mid = powit / 2 # 2 1
	levelp = level + 1 # 1 2
	for i in range(levelp):
		powlp = powit - pow(2,levelp) # 4 , 2 0
		#lpd = pow(2,level) # 0 , 2 pow(2,levelp) # 0 2
		midlp = powlp / 2 # 2 , 1 0
		pw = powit - midlp # 2 , 3 4
		map[powit-mid][powit-mid] = (map[powl][powl] + map[powl][powit] +map[powit][powit] +map[powit][powl]) /4.0
	
	
	for y in range(level*2):
		for x in range(level*2):
			print(map[x][y])
	if(iterations == level):
		return(map)
	else:
		return(generate_detail(level+1,map))
"""

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
	
	#return(map)
	print("==level" , level , "configuration==")
	render_map(map,0,0)
	print("==level", level,"configuration==")
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
	mid = (map[0][0]+map[1][0]+map[0][1]+map[1][1])/4 + random.uniform(-height/level,height/level)
	if(mid > 1.0):
		mid = 1.0
	if(mid < 0.0):
		mid = 0.0
	new_map = [[map[0][0],(map[0][0]+map[1][0])/2.0,map[1][0]],[(map[0][0]+map[0][1])/2,mid,(map[1][0]+map[1][1])/2],[map[0][1],(map[0][1]+map[1][1])/2,map[1][1]]]
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
	map = [[random.uniform(0.0,height),random.uniform(0.0,height)],[random.uniform(0.0,height),random.uniform(0.0,height)]]
#	map = [[random.uniform(0.0,0.3),random.uniform(0.0,0.3)],[random.uniform(0.0,0.3),random.uniform(0.0,0.3)]]
#	map = [[0.0,0.0],[0.0,0.0]]
	return(generate_level(1,map,height))
	
	
def render_quad(level,x,y,map_quad,alpha):
	global iterations,screen
	if(iterations > level +1):
		render_quad(level+1,x,y,map_quad[0],alpha)
		render_quad(level+1,x+pow(2,iterations-level-1),y,map_quad[1],alpha)
		render_quad(level+1,x,y+pow(2,iterations-level-1),map_quad[2],alpha)
		render_quad(level+1,x+pow(2,iterations-level-1),y+pow(2,iterations-level-1),map_quad[3],alpha)
		return
	#print(x,y)
	#print(map_quad)
	if(map_quad[0][0] > 0.6):
		screen.set_at((x+0,y+0),(map_quad[0][0] * 255,map_quad[0][0] * 255,map_quad[0][0] * 255,alpha))
	else:
		if(map_quad[0][0] < 0.2):
			screen.set_at((x+0,y+0),(20,20,map_quad[0][0] * 255,alpha))
		else:
			screen.set_at((x+0,y+0),(20,map_quad[0][0] * 255,20,alpha))
		
	if(map_quad[1][0] > 0.6):
		screen.set_at((x+1,y+0),(map_quad[1][0] * 255,map_quad[1][0] * 255,map_quad[1][0] * 255,alpha))
	else:
		if(map_quad[1][0] < 0.2):
			screen.set_at((x+1,y+0),(20,20,map_quad[1][0] * 255,alpha))
		else:
			screen.set_at((x+1,y+0),(20,map_quad[1][0] * 255,20,alpha))

			
	if(map_quad[0][1] > 0.6):
		screen.set_at((x+0,y+1),(map_quad[0][1] * 255,map_quad[0][1] * 255,map_quad[0][1] * 255,alpha))
	else:
		if(map_quad[0][1] < 0.2):
			screen.set_at((x+0,y+1),(20,20,map_quad[0][1] * 255,alpha))
		else:
			screen.set_at((x+0,y+1),(20,map_quad[0][1] * 255,20,alpha))

	if(map_quad[1][1] > 0.6):
		screen.set_at((x+1,y+1),(map_quad[1][1] * 255,map_quad[1][1] * 255,map_quad[1][1] * 255,alpha))
	else:
		if(map_quad[1][1] < 0.2):
			screen.set_at((x+1,y+1),(20,20,map_quad[1][1] * 255,alpha))
		else:
			screen.set_at((x+1,y+1),(20,map_quad[1][1] * 255,20,alpha))

	
	
"""	screen.set_at((x+0,y+0),(map_quad[0][0] * 255,map_quad[0][0] * 255,map_quad[0][0] * 255,alpha))
	screen.set_at((x+1,y+0),(map_quad[1][0] * 255,map_quad[1][0] * 255,map_quad[1][0] * 255,alpha))
	#screen.set_at((x+2,y+0),(map_quad[2][0] * 255,map_quad[2][0] * 255,map_quad[2][0] * 255))
	screen.set_at((x+0,y+1),(map_quad[0][1] * 255,map_quad[0][1] * 255,map_quad[0][1] * 255,alpha))
	screen.set_at((x+1,y+1),(map_quad[1][1] * 255,map_quad[1][1] * 255,map_quad[1][1] * 255,alpha))
	#screen.set_at((x+2,y+1),(map_quad[2][1] * 255,map_quad[2][1] * 255,map_quad[2][1] * 255))
	#screen.set_at((x+0,y+2),(map_quad[0][2] * 255,map_quad[0][2] * 255,map_quad[0][2] * 255))
	#screen.set_at((x+1,y+2),(map_quad[1][2] * 255,map_quad[1][2] * 255,map_quad[1][2] * 255))
	#screen.set_at((x+2,y+2),(map_quad[2][2] * 255,map_quad[2][2] * 255,map_quad[2][2] * 255))
#	screen.blit(filled_box,(bar*filled_box.get_width(),(playfield_size[1])*filled_box.get_height()))    	
"""
	
def render_map(map, offset_x,offset_y,alpha):
	render_quad(0,0,0,map,alpha)
	#render_quad(1,0,0,map[0],alpha)
	#render_quad(1,pow(2,iterations-1),0,map[1],alpha)
	#render_quad(1,0,pow(2,iterations-1),map[2],alpha)
	#render_quad(1,pow(2,iterations-1),pow(2,iterations-1),map[3],alpha)
	
	
	
	
def tick():pass
 
def pos2height_quad(level,x,y,qx,qy,map_quad):
	global iterations
	if(iterations > level +1):
		r = pos2height_quad(level+1,x,y,qx,qy,map_quad[0])
		if(r != -2.0):
			return(r)
		r = pos2height_quad(level+1,x,y,qx+pow(2,iterations-level-1),qy,map_quad[1])
		if(r != -2.0):
			return(r)
		r = pos2height_quad(level+1,x,y,qx,qy+pow(2,iterations-level-1),map_quad[2])
		if(r != -2.0):
			return(r)
		r = pos2height_quad(level+1,x,y,qx+pow(2,iterations-level-1),qy+pow(2,iterations-level-1),map_quad[3])
		if(r != -2.0):
			return(r)
		return -2.0
	#print(x,y,qx,qy)
	if(x>=qx and x < (qx + 1) and y>=qy and y<(qy+1)):
		#print(map_quad)
		return(map_quad[qx-x][qy-y])
	#return(map_
		
	return(-2.0)
	
""" get height @ pos"""
def pos2height(x,y,map):
	return(pos2height_quad(0,x,y,0,0,map))
	
def setheight_quad(level,x,y,height,qx,qy,map_quad):
	global iterations
	if(iterations > level +1):
		r = setheight_quad(level+1,x,y,height,qx,qy,map_quad[0])
		if(r == 1):
			return(1)
		r = setheight_quad(level+1,x,y,height,qx+pow(2,iterations-level-1),qy,map_quad[1])
		if(r == 1):
			return(1)
		r = setheight_quad(level+1,x,y,height,qx,qy+pow(2,iterations-level-1),map_quad[2])
		if(r == 1):
			return(1)
		r = setheight_quad(level+1,x,y,height,qx+pow(2,iterations-level-1),qy+pow(2,iterations-level-1),map_quad[3])
		if(r == 1):
			return(1)
		return(0)
	if(x>=qx and x < (qx + 1) and y>=qy and y<(qy+1)):
		map_quad[qx-x][qy-y] = height
		return(1)
	return(0)

	
""" get height @ pos"""
def setheight(x,y,height,map):
	setheight_quad(0,x,y,height,0,0,map)


def erode_step(x,y,map):
	pass
def erode(x,y,map):
	h_mm =pos2height(x,y,map)

	h_tl =pos2height(x-1,y-1,map)
	if(h_tl<h_mm):
		erode(x-1,y-1,map)
	h_tm =pos2height(x,y-1,map)
	if(h_tm<h_mm):
		erode(x,y-1,map)
	h_tr =pos2height(x+1,y-1,map)
	if(h_tr<h_mm):
		erode(x+1,y-1,map)

	h_ml =pos2height(x-1,y,map)
	if(h_ml<h_mm):
		erode(x-1,y,map)
	h_mr =pos2height(x+1,y,map)
	if(h_mr<h_mm):
		erode(x+1,y,map)

	h_bl =pos2height(x-1,y+1,map)
	if(h_bl<h_mm):
		erode(x-1,y+1,map)
	h_bm =pos2height(x,y+1,map)
	if(h_bm<h_mm):
		erode(x,y+1,map)
	h_br =pos2height(x+1,y+1,map)
	if(h_br<h_mm):
		erode(x+1,y+1,map)

	if(h_mm-0.1>=0.0):
		setheight(x,y,h_mm-0.1,map)
		
	

def setup():
	global screen
	random.seed()
	pygame.init()
	pygame.display.init()
	mixer.init()
	print("generating map")
	map = generate_map(1.0)
	#map2 = generate_map(0.8)
	#map3 = generate_map(0.6)
	#map4 = generate_map(0.6)
	#map5 = generate_map(0.4)
	print("generating done")
#	screen = pygame.display.set_mode((1024,768), 0, 32)
	screen = pygame.display.set_mode((640,480), 0, 32)
	screen.fill((120, 100, 80))
	pygame.display.flip ()
	pygame.init()
	button_down = False
	running = True
	offset_x = 0
	offset_y = 0
	#render_map(map,offset_x,offset_y)
	#return
	#render_map(map5,offset_x,offset_y,16)
	#render_map(map4,offset_x,offset_y,16)
	#render_map(map3,offset_x,offset_y,32)
	#render_map(map2,offset_x,offset_y,64)
	render_map(map,offset_x,offset_y,255)
	
	
	old_pos = pygame.mouse.get_pos()
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
			if(e.type == pygame.MOUSEBUTTONDOWN):
				button_down = True
			if(e.type == pygame.MOUSEBUTTONUP):
				button_down = False

		pygame.display.update()
		tick()
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
			#for i in range(10):
			#	erode(random.randint(0,pow(2,iterations-1)),random.randint(0,pow(2,iterations-1)),map)
			print("eroding done")
			#erode(pos[0],pos[1],map)
			render_map(map,offset_x,offset_y,255)
			h = pos2height(pos[0],pos[1],map)
			print(h)
			setheight(pos[0],pos[1],0.1122,map)
			h = pos2height(pos[0],pos[1],map)
			print(h)
			
	#			pos = (int(pos[0]/16),int(pos[1]/16))
	pygame.quit()

setup()