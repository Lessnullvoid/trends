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
import numpy as np
import sys, time
#import OSC,
import pygame
from pygame.locals import *
import argparse, cv2
from glob import glob
from random import randint
from bs4 import BeautifulSoup as BS

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


colors = [(12, 170, 66), (6, 147, 54), (51, 175, 93)]
ims = 0;
cc = colors[0]

##  --- ----- --- ----- --- ----- ---- ------ ---- --- - -- --- - - -- - - ##
if __name__ == "__main__":
	nn_ii = 0
	t = 0
	first = True
	# argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", 								help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=400, 		help="minimum area size")
	ap.add_argument("-i", "--img-dir", 			  default="./img/", help="image dir path")
	ap.add_argument("-s", "--snd-dir", 			  default="./snd/", help="sound dir path")
	args = vars(ap.parse_args())

	# osc
	#send_addr = "192.168.0.13", 8000
	#cOsc = OSC.OSCClient()
	#cOsc.connect(send_addr)
	#print "[t]: OSC : ok"

	# trends
	google_username = "minimaltecno78b@gmail.com"
	google_password = "terremoto88"
	path = ""
	pytrend = TrendReq(google_username, google_password, hl='es-MX', geo='MX', custom_useragent="RenzoTrend Script")
	# parse
	trending_searches = pytrend.trending_searches()
	articles = trending_searches['newsArticlesList']
	trends = [BS(ar[0]['title']).text for ar in articles]
	"""
	trends = ['Montana Earthquake Is Felt For Hundreds Of Miles Early Thursday',
			"Blac Chyna flashes ex Rob Kardashian's £200k gifts and poses with another man ...",
			"Andrew Garfield Faces Backlash After Saying 'I Am a Gay Man Right Now Just ...",
			"4 accused of fighting with officer on South Side"]
	"""
	t0 = time.time()
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
		cam = cv2.VideoCapture(1)
		time.sleep(1)
		grabbed, frame = cam.read()
	else:
		vid = cv2.VideoCapture(args["video"])
		grabbed, frame = vid.read()
	ff = None
	print "[t]: source :" + "CAM" if is_cam else "VIDEO"


	# pygame
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

	font = pygame.font.Font("Roboto-Regular.ttf", 35)
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
			# if not occupied turn off
			if cells[i]['count'] == 0:
				cells[i]['past'] = 0
				cells[i]['state'] = 0
			# if occupied count
			else:
				cells[i]['past'] += cells[i]['count']
				cells[i]['count'] = 0
				# if count>10 fade
				if cells[i]['past'] > 10:
					if cells[i]['state'] == 0:
						cells[i]['state'] = 1
						# seleccionar evento
						ant_ii = nn_ii
						#nn_ii = randint(0, len(img_list)-1)
						nn_tt = randint(0, len(trends)-1)
						nn_ss = randint(0, len(snd_list)-1)
						str_tt = trends[nn_tt]
						fade = 0
						snds[nn_ss].play()
					elif cells[i]['past'] < 255:
						fade = cells[i]['past']
						clock.tick(60)
						screen.set_alpha(fade)
						#screen.fill((0,0,0))
						# actualizar display
						#imgs[nn_ii].set_alpha(fade)
						#simg = imgs[nn_ii].get_size()
						#screen.blit(imgs[nn_ii], (disp_w/2-simg[0]/2, 0))
						# surface
						s.set_alpha(fade)
						s.fill((0,0,0))
						screen.blit(s, (0, disp_h-100))
						# draw
						size_text = font.size(str_tt)
						ren = font.render(str_tt, 1, c_w)
						screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h-50))
						pygame.display.update()

					else:
						fade = 255
						clock.tick(60)
						#screen.fill(c_b)
						simg = imgs[nn_ii].get_size()
						#screen.blit(imgs[nn_ii], (disp_w/2-simg[0]/2, 0))
						# surface
						s.fill((0,0,0))
						screen.blit(s, (0, disp_h-100))
						# draw
						size_text = font.size(str_tt)
						screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h-50))
						ren = font.render(str_tt, 1, c_w)
						pygame.display.update()
					#time.sleep(10)
				summ +=1;
				t = 0
				cc = colors[randint(0, len(colors)-1)]

		if summ==0:
			#go white
			clock.tick(60)
			if t<255: fade = 255-t
			else: fade =t-255
			t += 1
			if t>512:
				t = 0
				cc = colors[randint(0, len(colors)-1)]
				ims += 1
				if ims>len(trends)-1: ims = 0

			screen.set_alpha(255-fade)
			screen.fill(cc)

			size_text = font.size(trends[ims])
			ren = font.render(trends[ims], 1, c_w)
			screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h/2 - size_text[1]/2))

			ss.set_alpha(fade)
			ss.fill((0, 0, 0))
			screen.blit(ss, (0, 0))
			pygame.display.update()

		# update cada hora
		if time.time() - t0 > 3620:
			"""
			trends = ['Montana Earthquake Is Felt For Hundreds Of Miles Early Thursday',
			"Blac Chyna flashes ex Rob Kardashian's £200k gifts and poses with another man ...",
			"Andrew Garfield Faces Backlash After Saying 'I Am a Gay Man Right Now Just ...",
			"4 accused of fighting with officer on South Side"]
			"""
			trending_searches = pytrend.trending_searches()
			articles = trending_searches['newsArticlesList']
			trends = [BS(ar[0]['title']).text for ar in articles]

			t0 = time.time()
			print "[t]: trends : ok"

		# break?
		key = cv2.waitKey(1) & 0xFF
		if key == ord('n'):
			ff = gray_img
		if key == ord("q"):
			break
	## exit
	cv2.destroyAllWindows()
	pygame.quit()
