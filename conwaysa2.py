#!/usr/bin/env python
import os
import pygame
import random
from pygame.locals import *
import os.path, sys
import pygame.mixer, pygame.time
#from sys import stdout
#import curses
mixer = pygame.mixer
time = pygame.time

"""globals"""
image_dir = "./images"
bar = 0
max_bars = 32
empty_box = None
filled_box = None
screen = None


playfield_size = [max_bars,32]


playfield = [[False for x in range(playfield_size[0])] for y in range(playfield_size[1])]
playfield_samples = [None for y in range(playfield_size[1])]
playfield_channels = [None for y in range(playfield_size[1])]

def init_playfield(samples):
	global playfield,playfield_samples,playfield_size
	for i in range(190):
		x = random.randint(0,playfield_size[0]-1)
		y = random.randint(0,playfield_size[1]-1)
		playfield[y][x] = True
#	for y in range(playfield_size[1]):
#		for x in range(playfield_size[0]):
			#if(random.choice([True,False,False,False])):
#			if(random.randint(0,20) == 0):
#				sample = samples[random.randint(0,len(samples)-1)]
#				sound = mixer.Sound(sample)
#				playfield_samples[y][x] = sound 
#	for r in range(2):
	for i in range(len(samples)):
		sample = samples[i]
		sound = mixer.Sound(sample)
		if(i<playfield_size[1]):
			playfield_samples[i] = sound 



def display_playfield(bar):
	global empty_box,filled_box
	global playfield,playfield_size
	#screen.fill((120, 100, 80))
	for y in range(playfield_size[1]):
		for x in range(playfield_size[0]):
			if(playfield[y][x] == True):
				screen.blit(filled_box, (x*filled_box.get_width(), y*filled_box.get_height()))
			else:	
				screen.blit(empty_box, (x*filled_box.get_width(), y*filled_box.get_height()))
	for x in range(playfield_size[0]):
		screen.blit(empty_box,(x*filled_box.get_width(),(playfield_size[1])*filled_box.get_height()))    	
			

	screen.blit(filled_box,(bar*filled_box.get_width(),(playfield_size[1])*filled_box.get_height()))    	


def print_playfield(samples,bar):
	#print("\033[2J\033[0;0f")
	#print("\033[0;0f")
	#stdout.write(curses.tigetstr("clear"))
	#stdout.flush()
	global playfield,playfield_size
	print("+-" + "--"*(bar-1) + "**" + "--"*(max_bars-bar) + "+")
	#print("+-" + "--"*playfield_size[0] + "+")
	for y in range(playfield_size[1]):
		print("|", end=" ")
		for x in range(playfield_size[0]):
			if(playfield[y][x] == True):
				print("o", end=" ")
			else:
				print(".", end=" ")
		print("|", end=" ")
		if(y <len(samples)):		
			print(samples[y])
		else:
			print()
	#print("+-" + "--"*playfield_size[0] + "+")
	print("+-" + "--"*(bar-1) + "**" + "--"*(max_bars-bar) + "+")
#	print(playfield_samples)

def mutate_playfield():
	global playfield,playfield_samples,playfield_size
	for i in range(20):
		x = random.randint(0,playfield_size[0]-1)
		y = random.randint(0,playfield_size[1]-1)
		playfield[y][x] = True

def get_neighbours_num(x,y):
	global playfield,playfield_size
	n = 0
	if(y-1 >= 0 and playfield[y-1][x] == True):
		n += 1
	if(x-1 >= 0 and playfield[y][x-1] == True):
		n += 1
	if(x+1 < playfield_size[0] and playfield[y][x+1] == True):
		n += 1
	if(y+1 < playfield_size[1] and playfield[y+1][x] == True):
		n += 1

	if(y-1 >= 0 and x-1 > 0 and playfield[y-1][x-1] == True):
		n += 1
	if(y-1 >= 0 and x+1 < playfield_size[0] and playfield[y-1][x+1] == True):
		n += 1
	if(y+1 < playfield_size[1] and x+1 < playfield_size[0] and playfield[y+1][x+1] == True):
		n += 1
	if(y+1 < playfield_size[1] and x-1 >= 0 and playfield[y+1][x-1] == True):
		n += 1
	return n
	


def play_sounds(bar):
	global playfield,playfield_samples,playfield_size
	for y in range(playfield_size[1]):
		if(playfield[y][bar] == True and playfield_samples[y] != None):
				sample = playfield_samples[y];
				#if(
				if(playfield_channels[y] != None):
					sample.stop()
				playfield_channels[y] = sample.play()
				#sample.set_volume(random.randint(0,255))
				sample.set_volume(get_neighbours_num(bar,y)*20)
	


		

"""compute next step"""
def tick():
	global playfield,playfield_size
	new_playfield = [[False for x in range(playfield_size[0])] for y in range(playfield_size[1])]
	for y in range(playfield_size[1]):
		for x in range(playfield_size[0]):
			neighbours = get_neighbours_num(x,y)
			if(playfield[y][x] == True):
				if(neighbours < 2): #underpopulation
					new_playfield[y][x] = False
				if(neighbours == 2 or neighbours == 3): #great neighbourhood ,stay
					new_playfield[y][x] = True
				if(neighbours > 3): #overcrowded
					new_playfield[y][x] = False
			else:	
				if(neighbours == 3): #reproduce
					new_playfield[y][x] = True

	playfield = new_playfield

def get_samples(dir):
	files = os.listdir(dir)	
	for index,f in enumerate(files):
		f = dir + "/" +  f
		files[index] = f
	return files	

def setup():
	global bar,empty_box,filled_box,screen
	random.seed()
	pygame.init()
	pygame.display.init()
	mixer.init()
	#curses.setupterm()
	screen = pygame.display.set_mode((playfield_size[0]*16,(playfield_size[1]+1)*16 ), 0, 32)
	#screen = pygame.display.set_mode((1024,768), 0, 32)
	empty_box = pygame.image.load(os.path.join(image_dir, "empty_box.png")).convert()
	filled_box = pygame.image.load(os.path.join(image_dir, "box_num.png")).convert()


	screen.fill((120, 100, 80))
	pygame.display.flip ()
	samples = get_samples("./samples")
	init_playfield(samples)
	#tick()
	#print_playfield(samples,bar)
	pygame.init()
	#pygame.key.set_repeat (500, 30)
	#mixer.init(11025)
	#mixer.init(44100)
	#sample = samples[random.randint(0,len(samples)-1)]
	#print("playing sample:",sample)
	#sound = mixer.Sound(sample)
	#channel = sound.play()
	button_down = False
	running = True
	while running:
		for e in pygame.event.get():
			if(e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
				running = False
			if(e.type == pygame.MOUSEBUTTONDOWN):
				button_down = True
			if(e.type == pygame.MOUSEBUTTONUP):
				button_down = False

		#play_sounds(bar)
		#print_playfield(samples,bar)
		display_playfield(bar)
		#pygame.display.flip()
		pygame.display.update()
		#time.wait(int((1000*60)/80)) # 128bpm
		#time.wait(int(4000 / max_bars))
		time.wait(int( ( ((1000*60)/124)/max_bars) *4))
		bar += 1
		if(bar == max_bars):
			bar = 0
			#for i in range(2):	
			#mutate_playfield()
			#for i in range(3):
		tick()
		if(button_down):
			pos = pygame.mouse.get_pos()
			pos = (int(pos[0]/16),int(pos[1]/16))
			playfield[pos[1]][pos[0]] = True

	#while channel.get_busy(): #still playing
	#	print("  ...still going...")
	#	time.wait(1000)
	#print("...Finished")
	pygame.quit()

setup()