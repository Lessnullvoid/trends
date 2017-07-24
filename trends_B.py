#! /usr/bin/python
# -*-coding: UTF-8 -*-

"""
trends_B.py
----------
. connect to GtrendsAPI
. OSC server
. mono mode: stand by
.stand by:
	.constantly receives OSC messages from clients
	.creates buffer to read messages
	.alternatively fades from white
	.to color + centered trend text

"""

# packages
import sys, time
import OSC, pygame
import argparse, cv2
import threading
import numpy as np
from pytrends.request import TrendReq
from pygame.locals import *
from glob import glob
from random import randint
from bs4 import BeautifulSoup as BS

trends = []


# fnc
def get_cell_num(x, y):
	mon_w = 320
	mon_h = 240
	if x < mon_w/3:	cx = 0
	elif x > 2*mon_w/3: cx = 2
	else: cx = 1
	if y < mon_h/3: cy = 0
	elif y > 2*mon_h/3: cy = 2
	else: cy = 1
	index = 3*cy + cx
	return index

def print_info(cs):
	print "\t[c]:"
	for j in range(3):
		for i in range(3):
			index = 3*j + i
			#print '['+str(cs[index]["state"])+': '+str(cs[index]["past"])+': '+str(cs[index]["count"])+']\t',
			print '['+str(cs[index]["count"])+']\t',
		print ''


def cell_callback(path, tags, args, source):
	user = ''.join(path.split("/"))
	#no_cell = data.split("/")[1]
	txt = "[%d] :: %s" % (args[0], args[1])
	print txt
	trends.append(args[1])
	return

colors = [(60, 186, 84), (244, 194, 13), (219, 50, 54), (72, 133, 237)]
ims = 0;
cc = colors[0]

##  --- ----- --- ----- --- ----- ---- ------ ---- --- - -- --- - - -- - - ##
if __name__ == "__main__":
	nn_ii = 0
	t = 0
	first = True
	summ = 0
	# argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", 								help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=400, 		help="minimum area size")
	ap.add_argument("-i", "--img-dir", 			  default="./img/", help="image dir path")
	ap.add_argument("-s", "--snd-dir", 			  default="./snd/", help="sound dir path")
	args = vars(ap.parse_args())

	# osc
	recv_addr = "127.0.0.1", 10001
	s = OSC.OSCServer(recv_addr)
	s.addMsgHandler('/cell', cell_callback)
	st = threading.Thread(target=s.serve_forever)
	st.start()
	#s.serve_forever()
	print "[t]: OSC : ok"

	t0 = time.time()
	print "[t]: trends : ok"

	# resources directories
	snd_list = glob(args['snd_dir'] + "*.*")

	# display/pygame init
	disp_w = 1280
	disp_h = 720
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((disp_w, disp_h))
	pygame.display.set_caption('[trends]: display')
	pygame.mouse.set_visible(0)

	s = pygame.Surface((disp_w, 100))
	ss = pygame.Surface((disp_w, disp_h))

	font = pygame.font.Font("Roboto-Regular.ttf", 56)
	text = '[0FF]'
	size = font.size(text)
	c_w = 250, 240, 230
	c_b = 5, 5, 5

	screen.fill(c_b)
	ren = font.render(text, 1, c_w)
	screen.blit(ren, (disp_w/2 - size[0]/2, disp_h/2 - size[1]/2))
	pygame.display.update()
	print "[t]: display : 0FF"

	# get sounds
	snds = []
	for snd_name in snd_list:
		snds.append( pygame.mixer.Sound(snd_name) )
	print "[t]: snd_list :"+str(len(snd_list))

	# .the loop
	while True:
		# ----- ----- ------ ----- ----- NO DETECTION
		#cv2.imshow("[trends]: monitor", None)
		#go white
		clock.tick(60)
		if t<255: fade = 255-t
		else: fade =t-255
		t += 16
		if t>512:
			t = 0
			cc = colors[randint(0, len(colors)-1)]
			if (len(trends)>0 and ims<len(trends)):
				ims = -1
				if ims>len(trends)-1: ims = -1
		screen.set_alpha(255-fade)
		screen.fill(cc)

		if (len(trends)>0):
			size_text = font.size(trends[-1])
			ren = font.render(trends[-1], 1, c_w)
		else:
			size_text = font.size("0---0")
			ren = font.render("0---0", 1, c_w)

		if (len(trends)>5):
			trends = trends[-5:]

		screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h/2 - size_text[1]/2))

		ss.set_alpha(fade)
		ss.fill((255, 255, 255))
		screen.blit(ss, (0, 0))
		pygame.display.update()
		pygame.event.get()

		# break?
		key = cv2.waitKey(1) & 0xFF
		if key == ord('n'):
			ff = gray_img
		if key == ord("q"):
			break
	## exit
	cv2.destroyAllWindows()
	pygame.quit()
