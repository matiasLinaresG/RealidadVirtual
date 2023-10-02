# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import urllib.request
import cv2
import imutils
import time
import math


def camera_init():
	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space, then initialize the
	# list of tracked points
	yellow_lower = (20, 100, 100)
	yellow_upper = (30, 255, 255)

	# grab the reference
	# to the webcam
	vs = VideoStream(src=0).start()
	# vs = 1
	# allow the camera or video file to warm up
	time.sleep(2.0)

	return vs, yellow_lower, yellow_upper


def ball_detection(vs, lower, upper, show):

	# grab the current frame from url
	# url = "http://192.168.1.25:8080"
	# img_arr = np.array(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
	# frame = cv2.imdecode(img_arr, -1)
	# cv2.imshow('IPWebcam', frame)

	# grab frame from webcam
	frame = vs.read()
	# show the frame to our screen (use show=True for debug only)
	if show:
		cv2.imshow("yellowball", frame)
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		return 0
	# resize the frame, blur it, and convert it to the HSV
	# color space
	# frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,\
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

		real_radius = 50  # mm
		focal_length = 545  # radius(pixels) * 50cm / 5cm (test at 50cm distance with 2.5cm radius ball)

		dist = round((real_radius * focal_length)/radius)

		# theta = 2*math.atan(real_size/(2*focal_length))
		# dist = round(real_size / (2*math.tan(theta/2)))
		return center[0], center[1], dist
	else:
		return 0, 0, 0


def end_camera(vs):
	# release the camera
	# vs.release()
	# close all windows
	cv2.destroyAllWindows()


def run():
	vs, lower, upper = camera_init()
	while True:
		x, y, dist = ball_detection(vs, lower, upper, True)
		print(f"{x}, {y}, {dist}")
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			end_camera(vs)
			break

	print("Program ended by user")


#run()
