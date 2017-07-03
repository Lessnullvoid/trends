#! /usr/bin/python
# -*-coding: UTF-8 -*-

"""
trendyWindows
. divide el campo visual en 9 ventanas
. vigila la presencia de contours en cada una de ellas
. cuando encuentra algo en una celda despliega trendyinfo
"""

# packages
from pytrends.request import TrendReq
#import OSC
import pygame
from pygame.locals import *
import argparse
import cv2
from glob import glob
import numpy as np
import sys
import time
from random import randint

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


##  --- ----- --- ----- --- ----- ---- ------ ---- --- - -- --- - - -- - - ##
if __name__ == "__main__":

	# argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", 								help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=400, 		help="minimum area size")
	ap.add_argument("-i", "--img-dir", 			  default="./img/", help="image dir path")
	ap.add_argument("-s", "--snd-dir", 			  default="./snd/", help="sound dir path")
	args = vars(ap.parse_args())

	# osc
	send_addr = "192.168.0.13", 8000
	#cOsc = OSC.OSCClient()
	#cOsc.connect(send_addr)
	print "[t]: OSC : ok"

	# trends
	google_username = "microhom@gmail.com"
	google_password = "H0mh0mh0m2016!"
	path = ""
	kw_list=['temblor', 'terremoto', 'earthquake']
	pytrend = TrendReq(google_username, google_password, custom_useragent="RenzoTrend Script")
	pytrend.build_payload(kw_list=kw_list)
	related_queries_dict = pytrend.related_queries()
	print "[t]: trends : ok"

	# resources
	img_list = glob(args['img_dir'] + "*.*")
	snd_list = glob(args['snd_dir'] + "*.*")
	# get images
	imgs = []
	for img_name in img_list:
		imgs.append( pygame.image.load(img_name) )
	print "[t]: img_list :"+str(len(img_list))

	# source
	mon_w = 320
	mon_h = 240

	is_cam = True if (args['video'] == None) else False
	if (is_cam):
		cam = cv2.VideoCapture(0)
		time.sleep(1)
		grabbed, frame = cam.read()
	else:
		vid = cv2.VideoCapture(args["video"])
		grabbed, frame = vid.read()
	ff = None
	print "[t]: source :" + "CAM" if is_cam else "VIDEO"


	# pygame
	disp_w = 1000
	disp_h = 1000

	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((1000,1000))
	pygame.display.set_caption('[trends]: display')
	pygame.mouse.set_visible(0)

	font = pygame.font.Font("vcr_mono.ttf", 20)
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

	# model
	cells = []
	for i in range(9):
		cell = {"count":0, "past":0, "state":0}
		cells.append(cell);

	# .the loop
	while True:
		# get frame
		grabbed, frame = cam.read() if is_cam else vid.read()
		text = "OFF"

		# video end?
		if not grabbed:
			break

		# resize, grayscale, blur
		gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray_img = cv2.resize(gray_img, (mon_w, mon_h))
		gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)

		# first frame?
		if ff is None:
			ff = gray_img
			continue

		# diffs
		frame_delta = cv2.absdiff(ff, gray_img)

		frame_delta = ff - gray_img
		frame_delta = cv2.inRange(frame_delta, 10, 200)
		#th, thresh_img = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
		thresh_img = cv2.dilate(frame_delta, None, iterations=2)

		# contours
		contours, hie = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		big_cnts = [co for co in contours if cv2.contourArea(co) > args['min_area']]
		big_cnts = sorted(big_cnts, key = cv2.contourArea, reverse = True)

		for i in range(9):
			cells[i]['count'] = 0

		# loop over the contours
		for cnt in big_cnts:
			# locate by centroids
			M = cv2.moments(cnt)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			area = cv2.contourArea(cnt)

			# index cells
			index = get_cell_num(cx, cy)
			cells[index]['count'] += 1

			# draw monitor
			cv2.rectangle(frame_delta, (cx-10, cy-10), (cx+20, cy+20), (255,255,255))
		cv2.imshow("[trends]: monitor", frame_delta)

		print_info(cells)
		# update state
		summ = 0;
		for i in range(9):
			if cells[i]['count'] == 0:
				cells[i]['past'] = 0
				cells[i]['state'] = 0
			else:
				cells[i]['past'] += cells[i]['count']
				cells[i]['count'] = 0
				if cells[i]['past'] > 15 and cells[i]['state'] == 0:
					cells[i]['state'] = 1
					# seleccionar evento
					nn_ii = randint(0, len(img_list)-1)
					nn_tt = randint(0, len(kw_list)-1)
					nn_ss = randint(0, len(snd_list)-1)
					kw_tt = kw_list[nn_tt]
					str_tt = str(related_queries_dict[kw_tt]['top']).split('\n')
					# actualizar display
					clock.tick(60)
					screen.fill(c_b)
					screen.blit(imgs[nn_ii], (0, 0))
					yyy = 50;
					for st in str_tt:
						size = font.size(st)
						ren = font.render(st, 1, c_w)
						screen.blit(ren, (disp_w/2 - size[0]/2, yyy))
						yyy += 30
					pygame.display.update()
					snds[nn_ss].play()
					#time.sleep(10)

				summ +=1;
		if summ==0:
			clock.tick(60)
			screen.fill(c_b)
			pygame.display.update()
		#print_info(cells)

		# break?
		key = cv2.waitKey(1) & 0xFF
		if key == ord('n'):
			ff = gray_img
		if key == ord("q"):
			break
	## exit
	cv2.destroyAllWindows()
	pygame.quit()
