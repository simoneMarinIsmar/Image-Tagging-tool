#! /usr/bin/python

import sys
import numpy as np
import datetime as dt
import time
import multiprocessing as mp
import functools as ft
import cv2

#################################################

def getDate(strDay, strTime):
	# StrDay	2013:05:24
	# strTime	10:17:27

	if strDay and strTime:
		YYYY, MM, DD = strDay.split('-')
		hh, mm, ss = strTime.split(':')
		return dt.datetime(int(YYYY), int(MM), int(DD), int(hh), int(mm), int(ss))
	else:
		return None


def drawTaggs(event,x,y,flags,param):
	global drawing, eImg, img, posCnt, posDrawnBBs

	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		posCnt.append([x,y])

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			cv2.circle(img,(x,y),1,(0,0,0),-1)
			posCnt.append([x,y])

	elif event == cv2.EVENT_LBUTTONUP:
		if drawing == True:
			drawing = False
			cv2.circle(img,(x,y),1,(0,0,0),-1)
			posCnt.append([x,y])

			acnt = np.array(posCnt)
			rect = cv2.minAreaRect(acnt)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			cv2.drawContours(img,[box],0,(0,0,0),2)

			posDrawnBBs.append(box)
			posCnt = []


def manageTrackBar(val):
	global eImg, posCnt, posDrawnBBs

	if len(posDrawnBBs) == 0:
		if val >= 1:
			clahe = cv2.createCLAHE(clipLimit=val, tileGridSize=(4,4))
			eImg = clahe.apply(imGray)

		posDrawnBBs = []
		posCnt = []


def setUpImage():

	global winOrigName, winEnhanName, imgIndex, imGray, img, eImg

	winOrigName = 'Original '+ str(imgIndex+1)
	winEnhanName = 'Enhanced '+ str(imgIndex+1)

	if imgIndex < len(indicesDS):
		indices = indicesDS[imgIndex]-1
		img = cv2.imread(imgNames[indices])
		if img != []:
			cv2.imshow(winOrigName, img)
			imGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			print(imgNames[indices], '\t', imgDataSet[indices+1], '\t', imgIndex+1)
			# enhancing
			clahe = cv2.createCLAHE(clipLimit=clippingValue, tileGridSize=(4,4))
			eImg = clahe.apply(imGray)

			#show the image and attach the mouse callback
			#cv2.imshow(winEnhanName, eImg)
			cv2.setMouseCallback(winOrigName,drawTaggs)
			#cv2.createTrackbar('clipping', winEnhanName, clippingValue, 30, manageTrackBar)
		else:
			print ('error reading', imgNames[indices])
			sys.exit(1)
	else:
		print ('\nNo more images available\n')



def nextImg():
	global  winOrigName, winEnhanName, imgIndex, imGray, eImg, posDrawnBBs,\
		imgIndex, posCnt, totalTags

	# get tags
	if imgIndex < len(indicesDS):
		indices = indicesDS[imgIndex]-1
		date = imgDataSet[indices+1]
		imgTags = getImgTags(posDrawnBBs, date)
		print ('image tags = ', len(imgTags))
		totalTags.extend(imgTags)


		posDrawnBBs = []
		posCnt = []

		cv2.destroyAllWindows()
		imgIndex += 1
		setUpImage()


def getImgTags(posDrawnBBs, date):
	imgTags = []

	strDate = str(date.year)+':'+str(date.month)+':'+str(date.day)+'\t'\
			+str(date.hour)+':'+str(date.minute)+':'+str(date.second)
	for bb in posDrawnBBs:
		strBox = ', '.join(str(v[0])+', '+str(v[1]) for v in bb)
		row = imgNames[imgIndex]+'	'+strDate +'	'+strBox+'	' + input('pez: ')
		imgTags.append(row)

		outfile = open(outFileName, 'a')
		outfile.write(row)
		outfile.write('\n')
		print('tags:', str(imgTags))

	return imgTags


def writeTags(outFileName, outFileMode, totalTags):

	outfile = open(outFileName, outFileMode)
	for tag in totalTags:
		outFile.write(tag)

	outFile.close()


def usage():
	print ("USAGE: imageTagging.py outFile outFileMode imageList indicesFile imgIndex")
	print ('\t+ : next image \n\ts : save enhanced image\n\t<esc> : exit')

##################################################

if __name__ == "__main__":

	if len(sys.argv) == 6 and (sys.argv[2] == 'w' or sys.argv[2] == 'a'):

		# input parameters
		outFileName = sys.argv[1]
		outFileMode = sys.argv[2]
		imageList = sys.argv[3]
		indicesFileName = sys.argv[4]
		imgIndex = int(sys.argv[5])-1

		# global variables for mouse interaction
		ix,iy = -1,-1
		drawing = True # true if mouse is pressed
		posDrawnBBs = []
		posCnt = []
		totalTags = []
		clippingValue = 4


		# read input list
		imgNames = []
		imgDataSet = {}
		inFile = open(imageList, 'r')
		for row in inFile:
			dayTime, fullPath = row.split('\t')
			day, time = dayTime.split(' ')
			date = getDate(day, time)
			imgNames.append(fullPath.strip())
			imgDataSet[len(imgNames)] = date
		inFile.close()

		#read indicesFile
		indicesDS = []
		DSFile = open(indicesFileName, 'r')
		for row in DSFile:
			indicesDS.append(int(row.strip()))
		DSFile.close()

		# open output file
		outFile = open(outFileName, outFileMode)

		# seting up the image, the mouse and trackBar callbacks
		setUpImage()

		# loop for capturing mouse events
		while(1):
			cv2.imshow(winOrigName, img)
			#cv2.imshow(winEnhanName, eImg)
			#cv2.imwrite("C:\\Users\\Marco Francescangeli\\Desktop\\output_file\\" + str(imgIndex) + '.png', img)
			k = cv2.waitKey(1) & 0xFF
			if k == ord('e'): # the escape key
				print ('last image processed: ', imgIndex+1)
				break
			if k == ord('s'):
				cv2.imwrite("C:\\Users\\Marco Francescangeli\\Desktop\\output_file\\" + str(imgIndex) + '.png', img)
				print ('enhancedImg' + str(imgIndex) + '.png saved')

			elif k == ord('+'):
				nextImg()

		cv2.destroyAllWindows()

		# get tags
		if imgIndex < len(indicesDS):
			date = imgDataSet[indicesDS[imgIndex]+1]
			imgTags = getImgTags(posDrawnBBs, date)
			print ('image tags = aaaa', imgTags)
			totalTags.extend(imgTags)
			posDrawnBBs = []
			posCnt = []

		# write tags
		print ('total tags = ', len(totalTags))
		writeTags(outFileName, outFileMode, totalTags)

	else:
		usage()
		sys.exit(1)
