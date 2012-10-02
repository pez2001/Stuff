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


screen = None


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
	
def TriangleNormal(t):
	tu = Sub(t[1],t[0])
	tv = Sub(t[2],t[0])
	tn = Normalize(Cross(tu,tv))
	return(tn)
	
def Dot(a,b):
	return( (a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2]))


class frame:
	def __init__(self, sheet,offset,rect):
		self.sheet = sheet
		self.rect = rect
		self.offset = offset
	def draw(self,screen,pos):
		screen.blit(self.sheet,(pos[0]-self.offset[0],pos[1]-self.offset[1]),self.rect)

		
class multi_layer_frame:
	def __init__(self, frames):
		self.frames = frames
	def draw(self,screen,pos):
		for i in range(self.frames):
			i.draw(screen,pos)

			
class anim:
	def __init__(self,frames,anim_speed):
		self.anim_speed = anim_speed
		self.frames = frames
		self.frames_num = len(frames)
	def draw(self,screen,frame,pos):
		self.frames[frame].draw(screen,pos)
		
		
class static():
	def __init__(self,frames):
		#self.frames_len = len(frames)
		self.frames = frames
	def draw(self,screen,frame,pos):
		self.frames[frame].draw(screen,pos)

		
class screen_obj:
	def __init__(self,type,pos):
		self.pos = pos
		self.type = type
	def draw(self,screen):
		pass
	
		
class static_screen_obj(screen_obj):
	def __init__(self, statics,type,state,index,pos):
		self.pos = pos
		self.statics = statics
		self.type = type #"plant"
		self.state = state #"full_grown"
		self.index = index
	def update(self):
		pass
	def draw(self,screen):
		self.statics[self.state].draw(screen,self.index,self.pos)

		
class animated_static_screen_obj(screen_obj):
	def __init__(self,pos):
		self.pos = pos
		self.anims = anims
		self.type = "plant"
		self.state = "full_grown"
		self.action = "stand"

	
class moving_screen_obj(screen_obj):
	def __init__(self, anims,type,action,dir,movement_speed,pos):
		self.anims = anims
		self.type = type
		self.dir = dir
		self.action = action
		self.anim_step = 0
		self.anim_name = self.action+"_"+self.dir
		self.pos = pos
		self.movement_speed = movement_speed
		self.old_anim_ticks = pygame.time.get_ticks()
		self.old_move_ticks = pygame.time.get_ticks()
	def set_action(self,action):
		self.action = action
		self.anim_name = self.action+"_"+self.dir
		self.anim_step = 0
	def set_direction(self,dir):
		self.dir = dir
		self.anim_name = self.action+"_"+self.dir
	def update(self):
		ticks = pygame.time.get_ticks()

		if(ticks>self.old_anim_ticks+self.anims[self.anim_name].anim_speed):
			self.anim_step += 1
			self.old_anim_ticks = ticks
			if(self.anim_step>= self.anims[self.anim_name].frames_num):
				self.anim_step = 0

		if(self.movement_speed > 0 and ticks>self.old_move_ticks+self.movement_speed):
			if(self.dir == "right"):
				self.pos = (self.pos[0]+1,self.pos[1])
			if(self.dir == "up"):
				self.pos = (self.pos[0],self.pos[1]-1)
			if(self.dir == "left"):
				self.pos = (self.pos[0]-1,self.pos[1])
			if(self.dir == "down"):
				self.pos = (self.pos[0],self.pos[1]+1)
			self.old_move_ticks = ticks
	def draw(self,screen):
		self.anims[self.anim_name].draw(screen,self.anim_step,self.pos)


class tile:
	def __init__(self,pos):
		self.pos = pos

		
class tiles_set:
	def __init__(self, tile_sheet,tile_size,tiles):
		self.tile_sheet = tile_sheet
		self.tile_size = tile_size
		self.tiles = tiles
	def draw(self,screen,tile,index,pos):
		screen.blit(self.tile_sheet,pos,area = (self.tiles[tile][index].pos[0],self.tiles[tile][index].pos[1],self.tile_size[0],self.tile_size[1]))

		
def	draw_ground_layer(screen,offset,size):
	pass	
		
def tick():pass

def load_animation(char_pos,sprite_sheet):
	char_size = (16,18)
	
	char_anims = {}
	char_anims["stand_up"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+0,char_pos[1]+char_size[1]*0+0,char_size[0],char_size[1]))],0)
	char_anims["stand_right"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+0,char_pos[1]+char_size[1]*1+1,char_size[0],char_size[1]))],0)
	char_anims["stand_down"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+0,char_pos[1]+char_size[1]*2+1,char_size[0],char_size[1]))],0)
	char_anims["stand_left"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+0,char_pos[1]+char_size[1]*3+1,char_size[0],char_size[1]))],0)
	char_anims["walk_up"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*0+0,char_pos[1]+char_size[1]*0+0,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+1,char_pos[1]+char_size[1]*0+0,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*2+1,char_pos[1]+char_size[1]*0+0,char_size[0],char_size[1]))],80)
	char_anims["walk_right"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*0+0,char_pos[1]+char_size[1]*1+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+1,char_pos[1]+char_size[1]*1+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*2+1,char_pos[1]+char_size[1]*1+1,char_size[0],char_size[1]))],80)
	char_anims["walk_down"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*0+0,char_pos[1]+char_size[1]*2+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+1,char_pos[1]+char_size[1]*2+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*2+1,char_pos[1]+char_size[1]*2+1,char_size[0],char_size[1]))],80)
	char_anims["walk_left"] = anim([frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*0+0,char_pos[1]+char_size[1]*3+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*1+1,char_pos[1]+char_size[1]*3+1,char_size[0],char_size[1])),frame(sprite_sheet,(8,18),(char_pos[0]+char_size[0]*2+1,char_pos[1]+char_size[1]*3+1,char_size[0],char_size[1]))],80)
	return(char_anims)

def load_animations():

	#screen.blit(sprite_shadow,(m[i].pos[0],m[i].pos[1]+10),special_flags = BLEND_ADD)
	"""if(random.randint(0,100)>90):
		if(random.randint(0,100)>50):
			fp_layer.blit(sprite_footprints,(m[i].pos[0],m[i].pos[1]+1))
		else:
			fp_layer.blit(sprite_footprints,(m[i].pos[0],m[i].pos[1]+1),special_flags=BLEND_RGBA_SUB)
	screen.blit(sprite_shadow,(m[i].pos[0]-1,m[i].pos[1]+1))
	"""

	animations = {}
	sprite_shadow = pygame.image.load("game art//shadow.png").convert_alpha()
	sprite_footprints = pygame.image.load("game art//footprints.png").convert_alpha()
	sprite_footprints.set_alpha(10)
	sprite_sheet1 = pygame.image.load("game art//sprites_alpha.png").convert_alpha()
	sprite_sheet2 = pygame.image.load("game art//sprites_alpha2.png").convert_alpha()
	
	#sprite_sheet.set_colorkey()
	
	animations["monk_male"] = load_animation((16,180),sprite_sheet1)
	animations["berserk_male"] = load_animation((64,180),sprite_sheet1)
	animations["dknight_male"] = load_animation((112,180),sprite_sheet1)
	animations["soldier_male"] = load_animation((160,180),sprite_sheet1)
	animations["townfolk_male"] = load_animation((208,180),sprite_sheet1)
	animations["townfolk2_male"] = load_animation((256,180),sprite_sheet1)

	animations["monk_female"] = load_animation((16,306),sprite_sheet1)
	animations["berserk_female"] = load_animation((64,306),sprite_sheet1)
	animations["dknight_female"] = load_animation((112,306),sprite_sheet1)
	animations["soldier_female"] = load_animation((160,306),sprite_sheet1)
	animations["townfolk_female"] = load_animation((208,306),sprite_sheet1)
	animations["townfolk2_female"] = load_animation((256,306),sprite_sheet1)

	animations["warrior_male"] = load_animation((16,180),sprite_sheet2)
	animations["magician_male"] = load_animation((64,180),sprite_sheet2)
	animations["healer_male"] = load_animation((112,180),sprite_sheet2)
	animations["ninja_male"] = load_animation((160,180),sprite_sheet2)
	animations["ranger_male"] = load_animation((208,180),sprite_sheet2)
	animations["townfolk3_male"] = load_animation((256,180),sprite_sheet2)

	animations["warrior_female"] = load_animation((16,306),sprite_sheet2)
	animations["magician_female"] = load_animation((64,306),sprite_sheet2)
	animations["healer_female"] = load_animation((112,306),sprite_sheet2)
	animations["ninja_female"] = load_animation((160,306),sprite_sheet2)
	animations["ranger_female"] = load_animation((208,306),sprite_sheet2)
	animations["townfolk3_female"] = load_animation((256,306),sprite_sheet2)

	
	return(animations)

def load_tiles_set():
	tile_sheet = pygame.image.load("game art//tileset_1.png").convert_alpha()
	tiles = {}
	tiles["grass"] = (tile((16,16)),tile((8,56)),tile((8,136)))
	t = tiles_set(tile_sheet,(16,16),tiles)
	return(t)

def load_statics():
	
	tree_statics_sheet = pygame.image.load("game art//grassland_tiles.png").convert_alpha()
	statics = {}
	tree_statics = {}
	tree_statics["full_grown"] = static([frame(tree_statics_sheet,(62,160),(0,1164,124,180)),frame(tree_statics_sheet,(61,175),(130,1150,130,180)),frame(tree_statics_sheet,(61,175),(262,1150,130,180)),frame(tree_statics_sheet,(61,175),(392,1150,126,180)),frame(tree_statics_sheet,(81,136),(510,1192,138,148))])
	statics["tree"] = tree_statics
	return(statics)

def render_tiles_map(screen,tiles_set):
	for x in range(int(screen.get_width()/tiles_set.tile_size[0])):
		for y in range(int(screen.get_height()/tiles_set.tile_size[1])):
			index = random.randint(0,len(tiles_set.tiles["grass"])-1)
			tiles_set.draw(screen,"grass",index,(x*tiles_set.tile_size[0],y*tiles_set.tile_size[1]))

def setup():
	global screen
	random.seed()
	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.init()
	mixer.init()
	screen = pygame.display.set_mode((1024,1024), 0, 32)

	screen.fill((0, 0, 0))
	pygame.display.flip ()
	
	animations = load_animations()
	statics = load_statics()
	tiles_set = load_tiles_set()
	

	bg_layer = pygame.Surface((screen.get_width(),screen.get_height()),flags = SRCALPHA)
	fp_layer = pygame.Surface((screen.get_width(),screen.get_height()),flags = SRCALPHA)
	render_tiles_map(bg_layer,tiles_set)
	
	chars = ("monk_male","berserk_male","dknight_male","soldier_male","townfolk_male","townfolk2_male","monk_female","berserk_female","dknight_female","soldier_female","townfolk_female","townfolk2_female","warrior_male","magician_male","healer_male","ninja_male","ranger_male","townfolk3_male","warrior_female","magician_female","healer_female","ninja_female","ranger_female","townfolk3_female")
	trees_num = 200
	units_num = 1000
	objects = [ None for i in range(units_num+trees_num)]
	for i in range(units_num):
		objects[i] = moving_screen_obj(animations[random.choice(chars)],"char","walk",random.choice(("left","right","up","down")),random.randint(20,60),(random.randint(0,1000),random.randint(0,1000)))
	for i in range(trees_num):
		index = random.randint(0,len(statics["tree"]["full_grown"].frames)-1)
		objects[units_num+i] = static_screen_obj(statics["tree"],"tree","full_grown",index,(random.randint(0,1000),random.randint(0,1000)))
		
	#grass_tiles = pygame.image.load("game art//").convert()
	#water_tiles = pygame.image.load("game art//graphics-tiles-waterflow").convert()
	#fp_layer.set_alpha(14)

	button_down = False
	running = True
	offset_x = 0
	offset_y = 0
	old_pos = pygame.mouse.get_pos()
	
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
			if(e.type == pygame.MOUSEBUTTONDOWN):
				button_down = True
			if(e.type == pygame.MOUSEBUTTONUP):
				button_down = False

		#screen.fill((0, 0, 0))
		#render_ground_layer(screen,(offset_x,offset_y),(1000,1000))
		screen.blit(bg_layer,(0,0))
		screen.blit(fp_layer,(0,0))
		

		objects = sorted(objects,key = lambda screen_object: screen_object.pos[1],reverse=False)
		for i in range(len(objects)):
			#if(objects[i].type == "tree"):
			#	print("tree@",i)
			objects[i].draw(screen)
			objects[i].update()		
			if(objects[i].type == "char"):
				c = random.randint(0,100)
				if(c>99):
						objects[i].set_action("stand")
						objects[i].set_direction(random.choice(("left","right","up","down")))
						objects[i].movement_speed = 0
				
				else:
					if(c > 95):
						objects[i].set_action("walk")
						objects[i].set_direction(random.choice(("left","right","up","down")))
						objects[i].movement_speed = random.randint(20,60)

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


	pygame.quit()

setup()