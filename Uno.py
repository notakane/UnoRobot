import cv2
import numpy as np

print "LOADING............"

redCard = cv2.imread('red.jpg')
hsv = cv2.cvtColor(redCard, cv2.COLOR_BGR2HSV)
redHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

yellowCard = cv2.imread('yellow.jpg')
hsv = cv2.cvtColor(yellowCard, cv2.COLOR_BGR2HSV)
yellowHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

greenCard = cv2.imread('green.jpg')
hsv = cv2.cvtColor(greenCard, cv2.COLOR_BGR2HSV)
greenHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

blueCard = cv2.imread('blue.jpg')
hsv = cv2.cvtColor(blueCard, cv2.COLOR_BGR2HSV)
blueHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

wildCard = cv2.imread('wild.jpg')
hsv = cv2.cvtColor(wildCard, cv2.COLOR_BGR2HSV)
wildHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

histogramArray = [redHist, yellowHist, greenHist, blueHist, wildHist]

zero = cv2.imread('0.jpg',0)
one = cv2.imread('1.jpg',0)
two = cv2.imread('2.jpg',0)
three = cv2.imread('3.jpg',0)
four = cv2.imread('4.jpg',0)
five = cv2.imread('5.jpg',0)
six = cv2.imread('6.jpg',0)
seven = cv2.imread('7.jpg',0)
eight = cv2.imread('8.jpg',0)
nine = cv2.imread('9.jpg',0)
reverse = cv2.imread('reverse.jpg',0)
skip = cv2.imread('skip.jpg',0)
draw2 = cv2.imread('draw2.jpg',0)
draw4 = cv2.imread('draw4.jpg',0)
wild = cv2.imread('wil.jpg',0)

cardTypes = [zero, one, two, three, four, five,
			 six, seven, eight, nine, reverse,
			 skip, draw2, draw4, wild]

sift = cv2.xfeatures2d.SIFT_create()

typeFeatures = []


for x in range(0,15):
	kp2, des2 = sift.detectAndCompute(cardTypes[x], None)
	typeFeatures.append(kp2)
	typeFeatures.append(des2)
	if x==5:
		print "STILL LOADING......"
	if x==10:
		print "ALMOST THERE......."



def drawCard():
	print("drawn lol")


def findColorMatch(frame):
	# Calculate color match
	frameImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	frameHistogram = cv2.calcHist([frameImage],[0,1],None,[256,256],[0,256,0,256])
	histogramResult = 1

	for x in range(0,5):
		res = cv2.compareHist(frameHistogram, histogramArray[x], cv2.HISTCMP_HELLINGER)
		if res < histogramResult:
			histogramResult = res
			histogramIndex = x

	if histogramIndex == 0:
		print "Red card detected!"
	elif histogramIndex == 1:
		print "Yellow card detected!"
	elif histogramIndex == 2:
		print "Green card detected!"
	elif histogramIndex == 3:
		print "Blue card detected!"
	elif histogramIndex == 4:
		print "Wild card detected!"

def findTypeMatch(frame):
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	bf = cv2.BFMatcher()

	kp, des = sift.detectAndCompute(grayFrame, None)
	
	numMatches = 0
	matchIndex = 0

	for x in range(0,29, 2):
		kp2 = typeFeatures[x]
		des2 = typeFeatures[x+1]

		matches = bf.knnMatch(des, des2, k=2)
		good = []
		for m,n in matches:
			if m.distance < 0.45*n.distance:
				good.append([m])

		if len(good) > numMatches:
			numMatches = len(good)
			matchIndex = x/2

	print "This image matched to index #", matchIndex

def main():
	cap = cv2.VideoCapture(1)



	while(True):
		if(cap.isOpened() == False):
			print("Error!")
			break

		ret, frame = cap.read()
		if(ret == True):
			#findColorMatch(frame)
			findTypeMatch(frame)
				
		cv2.imshow("Camera", frame)

		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break
			

		

	cap.release()

if __name__ == '__main__':
	main()
