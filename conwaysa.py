#!/usr/bin/env python
import os
import pygame
import random
from pygame.locals import *
import os.path, sys
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time

"""globals"""
playfield_size = [78,38]


playfield = [[False for x in range(playfield_size[0])] for y in range(playfield_size[1])]
playfield_samples = [["" for x in range(playfield_size[0])] for y in range(playfield_size[1])]
playfield_channels = [[None for x in range(playfield_size[0])] for y in range(playfield_size[1])]

def init_playfield(samples):
	global playfield,playfield_samples,playfield_size
	for i in range(390):
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
	for r in range(1):
		for i in range(len(samples)):
			x = random.randint(0,playfield_size[0]-1)
			y = random.randint(0,playfield_size[1]-1)
			sample = samples[i]
			sound = mixer.Sound(sample)
			playfield_samples[y][x] = sound 

	

def print_playfield():
	global playfield,playfield_size
	print("+-" + "--"*playfield_size[0] + "+")
	for y in range(playfield_size[1]):
		print("|", end=" ")
		for x in range(playfield_size[0]):
			if(playfield[y][x] == True):
				print("o", end=" ")
			else:
				print(".", end=" ")
		print("|")
	print("+-" + "--"*playfield_size[0] + "+")
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
	


def play_sounds():
	global playfield,playfield_samples,playfield_size
	for y in range(playfield_size[1]):
		for x in range(playfield_size[0]):
			if(playfield[y][x] == True and playfield_samples[y][x] != ""):
				sample = playfield_samples[y][x];
				#if(
				if(playfield_channels[y][x] != None):
					sample.stop()
				playfield_channels[y][x] = sample.play()
				#sample.set_volume(random.randint(0,255))
				sample.set_volume(get_neighbours_num(x,y)*20)
	


		

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
	random.seed()
	mixer.init()
	#screen = pygame.display.set_mode ((640, 480), 0, 32)
	samples = get_samples("./samples")
	init_playfield(samples)
	tick()
	print_playfield()
	pygame.init ()
	#screen.fill ((100, 100, 100))
	#pygame.display.flip ()
	#pygame.key.set_repeat (500, 30)
	#mixer.init(11025)
	#mixer.init(44100)
	#sample = samples[random.randint(0,len(samples)-1)]
	#print("playing sample:",sample)
	#sound = mixer.Sound(sample)
	#channel = sound.play()

	while True:
		play_sounds()
		#for i in range(2):	
		mutate_playfield()
		tick()
		print_playfield()
		#time.wait(int((1000*60)/80)) # 128bpm
		time.wait(50)

	#while channel.get_busy(): #still playing
	#	print("  ...still going...")
	#	time.wait(1000)
	#print("...Finished")
	pygame.quit()

setup()