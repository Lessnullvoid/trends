# USAGE
# python main.py (lectura de camara)

# import the necessary packages
import argparse
import datetime
import imutils
import time
import math
import cv2
import OSC
import numpy
import pyglet
from pytrends.request import TrendReq


# enter your own credentials
google_username = "microhom@gmail.com"
google_password = "H0mh0mh0m2016!"
path = ""

#Login to google
pytrend = TrendReq(google_username,
                        google_password,
                        custom_useragent="RenzoTrend Script")
#capture API tokens
pytrend.build_payload(kw_list=['temblor', 'heartquake', 'terremoto'])

# osc init
send_addr = "192.168.1.37", 57120
cOsc = OSC.OSCClient()
cOsc.connect(send_addr)

#window and graphics
window = pyglet.window.Window()
label = pyglet.text.Label('PRINT TRENDS',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area",
                        type=int,
                        default=500,
                        help="minimum area size")

args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "OFF"


	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(),
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
		text = "ON"
        # send osc message to start_sample
        if OSCMessage == "ON"
        msg = OSC.OSCMessage()
        msg.setAddress("/1")
        msg.append(1)
        cOsc.send(msg)

        msg = OSC.OSCMessage()
        msg.setAddress("/1")
        msg.append(0)


	# draw the text and timestamp on the frame
	cv2.putText(frame, "Estado del sensor: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Sensor Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF




	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
pyglet.app.run()


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
