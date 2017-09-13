#! /usr/bin/python
# -*-coding: UTF-8 -*-



"""
trends_A.py
----------
. connect to GtrendsAPI
. dual mode: active, stand by
.active mode:
	.check for presence on 3x3 webcam grid
	.when something present select trend, image, sound and display
	.also send message to trendsB.oy
.stand by:
	.alternatively fades from white
	.to color + centered trend text

[CHI]: 0 Raspberry Pi con Chile de tendencia.
[IND]: 1 Raspberry Pi con Indonesia de tendencia.
[JPN]: 2 Raspberry Pi con Japón de tendencia.
[RUS]: 3 Raspberry Pi con Rusia de tendencia.
[USA]: 4 Raspberry Pi con EEUU de tendencia.
[ICE]: 5 Raspberry Pi con Islandia de tendencia (si Islandia no estan en Trends usar Nueva Zelanda).
[MEX]: 6 Raspberry Pi con México de tendencia.


-execute with arguments:

-sudo python /home/pi/trends/trends_A.py -i "./img/" -s "./snd/" -r "192.168.1.109" -p "10001" -g "MEX"

orden de las caperpetas de audio y video

-img:
-img01 = Chile
-img02 = Chile
-img03 = Rusia
-img04 = Chile
-img05 = Indonesia
-img06 = Mexico
-img07 = Japon
-img08 = EEUU
-img09 = NewZeland
-
-snd:
-snd01 = Chile
-snd02 = Chile
-snd03 = Rusia
-snd04 = Chile
-snd05 = Indonesia
-snd06 = Mexico
-snd07 = Japon
-snd08 = EEUU
-snd09 = Islandia

- NOTAS PARA CORREGIR
Los sonidos deben sumarse
La imagen dedebe desaparecer en cuanto aparece sin dejar de sonar el sonido
Hacer la letra uppercase

"""


# packages
from pytrends.request import TrendReq
import numpy as np
import sys, time
import OSC, pygame
from pygame.locals import *
import argparse, cv2
from glob import glob
from random import randint
from bs4 import BeautifulSoup as BS

# fnc
def get_cell_num(x, y):
	mon_w = 320
	mon_h = 240
	if x < mon_w: cx = 0
	if y < mon_h: cy = 0
	index = 3*cy + cx
	return index

#def get_cell_num(x, y):
	#mon_w = 320
	#mon_h = 240
	#if x < mon_w/3:	cx = 0
	#elif x > 2*mon_w/3: cx = 2
	#else: cx = 1
	#if y < mon_h/3: cy = 0
	#elif y > 2*mon_h/3: cy = 2
	#else: cy = 1
	#index = 3*cy + cx
	#return index

def print_info(cs):
	print "\t[c]:"
	for j in range(3):
		for i in range(3):
			index = 3*j + i
			print '['+str(cs[index]["state"])+': '+str(cs[index]["past"])+': '+str(cs[index]["count"])+']\t',
			#print '['+str(cs[index]["count"])+']\t',
		print ''

def send_actual(cell_no, trend_str, cOsc):
	"""form and send osc messahe"""
	route = "/cell"
	d = str(trend_str)
	msg = OSC.OSCMessage()
	msg.setAddress(route)
	msg.append(cell_no)
	msg.append(d)
	cOsc.send(msg)
	print "[OSC]: " + "<<" + route + "::" + d

def splitlines (t):
	if len(t)<20:
		return 1, [str(t)]
	elif len(t)>20 and len(t)<40:
		ls = t.split(' ')
		h = len(ls)
		a = ' '.join(ls[:int(h/2)])
		b = ' '.join(ls[int(h/2):])
		return 2, [str(a), str(b)]
	else:
		ls = t.split(' ')
		h = len(ls)
		a = ' '.join(ls[:int(h/3)])
		b = ' '.join(ls[int(h/3):int(2*h/3)])
		c = ' '.join(ls[int(2*h/3):])
		return 3, [str(a), str(b), str(c)]



def byreg(alltren, reg):
	return [alltren[i] for i in range(len(alltren)) if i%7==rix[reg] or i%7==abs(rix[reg]-1)]




colors = [(40, 158, 0), (40, 158, 0), (40, 158, 0), (40, 158, 0)]
ims = 0;
cc = colors[0]

##  --- ----- --- ----- --- ----- ---- ------ ---- --- - -- --- - - -- - - ##
if __name__ == "__main__":
	nn_ii = 0
	t = 0
	first = True
	rix = {'CHI':0, 'IND':1, 'JPN':2, 'RUS':3, 'USA':4, 'ICE':5, 'MEX':6}
	# argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", 											help="path to the video file")
	ap.add_argument("-a", "--min-area",	type=int, 	default=400, 				help="minimum area size")
	ap.add_argument("-i", "--img-dir",				default="./img/",			help="image dir path")
	ap.add_argument("-s", "--snd-dir",				default="./snd/",			help="sound dir path")
	ap.add_argument("-r", "--receiver-ip",			default="127.0.0.1",		help="receiver ip address")
	ap.add_argument("-p", "--receiver-port",		default="10001",			help="receiver osc port")
	ap.add_argument("-g", "--region",				default="CHI",				help="regions: CHI, IND, JPN, RUS, USA, ICE, MEX")
	ap.add_argument("-l", "--local",				default="False",			help="if != None, uses file as input trends")

	args = vars(ap.parse_args())

	# osc
	send_addr = args["receiver_ip"], int(args["receiver_port"])
	cOsc = OSC.OSCClient()
	cOsc.connect(send_addr)
	print "[t]: OSC : ok"

	# trends
	region = args["region"]
	use_local = args["local"] if args["local"] != "False" else False

	if not use_local:
		google_username = "minimaltecno78b@gmail.com"
		google_password = "terremoto88"
		path = ""
		pytrend = TrendReq(google_username, google_password, hl='es-MX', geo='MX', custom_useragent="Trend Script")
		# parse
		trending_searches = pytrend.trending_searches()
		articles = trending_searches['title']
		#trends = articles
		trends = byreg(articles, region)
	else:
		trends = [tr.strip().rstrip() for tr in open(use_local, 'r').readlines()]

	t0 = time.time()
	print "[t]: trends : ok"

	# resources directories
	img_list = glob(args['img_dir'] + "*.*")
	snd_list = glob(args['snd_dir'] + "*.*")

	# monitor/video source
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

	# Aqui se ajusta el tamanano de la pantalla
	disp_w = 1280
	disp_h = 1024
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	clock = pygame.time.Clock()
	#screen = pygame.display.set_mode((disp_w, disp_h))
	screen = pygame.display.set_mode((disp_w, disp_h), pygame.FULLSCREEN)
	pygame.display.set_caption('[trends]: display')
	pygame.mouse.set_visible(0)

	s = pygame.Surface((disp_w, 110))
	ss = pygame.Surface((disp_w, disp_h))


	font = pygame.font.Font("arial.ttf", 150) #Aqui se ajusta el tamano del font
	text = '[0FF]'
	size = font.size(text)
	c_w = 250, 240, 230
	c_b = 5, 5, 5

	screen.fill(c_b)
	ren = font.render(text, 1, c_w)
	screen.blit(ren, (disp_w/2 - size[0]/2, disp_h/2 - size[1]/2))
	pygame.display.update()
	print "[t]: display : 0FF"

	# get images
	imgs = []
	for img_name in img_list:
		imgs.append( pygame.image.load(img_name) )
	print "[t]: img_list :"+str(len(img_list))

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
		# ----- ----- ------ ----- ----- DETECT PRESENCE
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
		# find differences
		#frame_delta = cv2.absdiff(ff, gray_img)
		frame_delta = ff - gray_img
		frame_delta = cv2.inRange(frame_delta, 10, 200)
		#th, thresh_img = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
		thresh_img = cv2.dilate(frame_delta, None, iterations=2)
		# contours
		contours, hie = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		big_cnts = [co for co in contours if cv2.contourArea(co) > args['min_area']]
		big_cnts = sorted(big_cnts, key = cv2.contourArea, reverse = True)
		# init cells
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
			# rectangles
			cv2.rectangle(frame_delta, (cx-10, cy-10), (cx+20, cy+20), (255,255,255))
		# draw monitor
		#cv2.imshow("[trends]: monitor", frame_delta)		#comment this line to hide monitor window
		print_info(cells)
		# update state
		summ = 0;
		for i in range(9):
			# if not occupied turn off
			if cells[i]['count'] == 0:
				cells[i]['past'] = 0
				cells[i]['state'] = 0
			# if occupied count
			elif cells[i]['state']<2:
				cells[i]['past'] += cells[i]['count']
				cells[i]['count'] = 0
				# if count>10 fade
				if (cells[i]['past'] > 10):
					if cells[i]['state'] == 0:
						cells[i]['state'] = 1
						# seleccionar evento
						ant_ii = nn_ii
						nn_ii = randint(0, len(img_list)-1)
						nn_tt = randint(0, len(trends)-1)
						nn_ss = randint(0, len(snd_list)-1)
						line_tt = trends[nn_tt]
						n_tt, strs_tt = splitlines(line_tt)
						fade = 0
						snds[nn_ss].play()
						# send OSC
						send_actual(i, line_tt, cOsc)
					elif (cells[i]['state']==1 and cells[i]['past'] < 10):
						fade = cells[i]['past']*10
						clock.tick(60)
						#background
						ss.set_alpha(fade)
						ss.fill((0,0,0))
						screen.blit(ss, (0, 0))
						#img
						screen.set_alpha(fade)
						#screen.fill((0,0,0))
						# actualizar display
						imgs[nn_ii].set_alpha(fade)
						simg = imgs[nn_ii].get_size()
						screen.blit(imgs[nn_ii], (disp_w/2-simg[0]/2, 0))
						# surface
						#s.set_alpha(fade)
						#s.fill((0,0,0))
						#screen.blit(s, (0, disp_h-100))
						# draw
						#for n,str_tt in enumerate(strs_tt):
							#size_text = font.size(str_tt)
							#surface
							#s.set_alpha(fade)
							#s.fill((0,0,0))
							#text
							#ren = font.render(str_tt, 1, c_w)
							#distache = 0
							#if n_tt==3: distache = disp_h-(3-n)*size_text[1]
							#if n_tt==2: distache = disp_h-(2-n)*size_text[1]
							#if n_tt==1: distache = disp_h-(1-n)*size_text[1]
							#screen.blit(s, (0, distache))
							#screen.blit(ren, (disp_w/2 - size_text[0]/2, distache))
						pygame.display.update()

					elif (cells[i]['state']==1 and cells[i]['past'] >= 10 and cells[i]['past'] < 12):
						fade = 255
						clock.tick(60)
						#screen.fill(c_b)
						simg = imgs[nn_ii].get_size()
						screen.blit(imgs[nn_ii], (disp_w/2-simg[0]/2, 0))
						# surface
						#s.fill((0,0,0))
						#screen.blit(s, (0, disp_h-100))
						# draw
						#for n,str_tt in enumerate(strs_tt):
							#size_text = font.size(str_tt)
							#surface
							#s.set_alpha(fade)
							#s.fill((0,0,0))
							#text
							#ren = font.render(str_tt, 1, c_w)
							#distache = 0
							#if n_tt==3: distache = disp_h-(3-n)*size_text[1]
							#if n_tt==2: distache = disp_h-(2-n)*size_text[1]
							#if n_tt==1: distache = disp_h-(1-n)*size_text[1]
							#screen.blit(s, (0, distache))
							#screen.blit(ren, (disp_w/2 - size_text[0]/2, distache))
						pygame.display.update()
					elif  cells[i]['past'] > 127:
						cells[i]['state'] = 4
						#cells[i]['past'] = 0
						#summ = 0
					#time.sleep(10)
				summ +=1;
				t = 0
				cc = colors[randint(0, len(colors)-1)]

		if summ==0:
			#go white
			clock.tick(60)
			if t<255: fade = 255-t
			elif t>512: fade = t-512
			else: fade = 0
			t += 22											#this controls fade velocity
			if t>767:
				t = 0
				cc = colors[randint(0, len(colors)-1)]
				ims += 1
				if ims>len(trends)-1: ims = 0

			screen.set_alpha(255-fade)
			screen.fill(cc)

			#str_nn = splitlines(trends[ims])
			#size_text = font.size(str_nn)
			#ren = font.render(str_nn, 1, c_w)
			#screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h/2 - size_text[1]/2))
			line_tt = trends[ims]
			n_tt, strs_tt = splitlines(line_tt)
			for n,str_tt in enumerate(strs_tt):
				size_text = font.size(str_tt)
				ren = font.render(str_tt, 1, c_w)
				screen.blit(ren, (disp_w/2 - size_text[0]/2, disp_h/2 - (1-n)*size_text[1]))
			ss.set_alpha(fade)
			ss.fill((255, 255, 255))
			screen.blit(ss, (0, 0))
			pygame.display.update()

		# update cada hora
		if time.time() - t0 > 3620:

			try:
				trending_searches = pytrend.trending_searches()
				#articles = trending_searches['newsArticlesList']
				#trends = [BS(ar[0]['title'], "lxml").text for ar in articles]
				articles = trending_searches['title']
				#trends = articles
				trends = byreg(articles, region)

				print "[t]: trends : ok"
			except:
				print "[x]: trends : could not update trends"

			t0 = time.time()

		# break?
		pygame.event.get()
		key = cv2.waitKey(1) & 0xFF
		if key == ord('n'):
			ff = gray_img
		if key == ord("q"):
			break
	## exit
	cv2.destroyAllWindows()
	pygame.quit()
