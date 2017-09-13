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

	sudo python /home/pi/trends/trends_C.py -r "192.168.0.23" -p "10001"

	sudo python /home/pi/trends/trends_A.py -i "./img01/" -s "./snd01/" -r "192.168.0.23" -p "10001" -g "CHI" -l "chi.txt"

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
			#print '['+str(cs[index]["count"])+']\t',
		print ''


def cell_callback(path, tags, args, source):
	user = ''.join(path.split("/"))
	#no_cell = data.split("/")[1]
	#txt = "[%d] :: %s" % (args[0], args[1])
	#print txt
	trends.append(args[1])
	#play a sound each time
	#nn_ss = randint(0, len(snd_list)-1)
	#snds[nn_ss].play()
	return

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


#colors = [(60, 186, 84), (244, 194, 13), (219, 50, 54), (72, 133, 237)]
colors = [(40, 158, 0), (40, 158, 0), (40, 158, 0), (40, 158, 0)]

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
	ap.add_argument("-s", "--snd-dir", 			  default="./snd01/", help="sound dir path")
	ap.add_argument("-r", "--local-ip",			default="127.0.0.1",		help="local ip address")
	ap.add_argument("-p", "--local-port",		default="10001",			help="local osc port")

	args = vars(ap.parse_args())

	# osc
	#recv_addr = "127.0.0.1", 10001
	recv_addr = args["local_ip"], int(args["local_port"])
	s = OSC.OSCServer(recv_addr)
	s.addMsgHandler('/cell', cell_callback)
	st = threading.Thread(target=s.serve_forever)
	st.start()
	#s.serve_forever()
	print "[t]: OSC Reciber C connected"

	t0 = time.time()
	print "[t]: trends Reciber C connected"



	# .the loop
	while True:


		# break?
		#pygame.event.get()
		key = cv2.waitKey(1) & 0xFF
		if key == ord('n'):
			ff = gray_img
		if key == ord("q"):
			break
	## exit
	cv2.destroyAllWindows()
	pygame.quit()
