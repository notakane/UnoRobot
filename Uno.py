import cv2
import time

print "INITIALIZING......."

handOfCards = [("YELLOW",4), ("GREEN",0)]


redCard = cv2.imread('./CardColors/red.jpg')
hsv = cv2.cvtColor(redCard, cv2.COLOR_BGR2HSV)
redHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

yellowCard = cv2.imread('./CardColors/yellow.jpg')
hsv = cv2.cvtColor(yellowCard, cv2.COLOR_BGR2HSV)
yellowHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

greenCard = cv2.imread('./CardColors/green.jpg')
hsv = cv2.cvtColor(greenCard, cv2.COLOR_BGR2HSV)
greenHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

blueCard = cv2.imread('./CardColors/blue.jpg')
hsv = cv2.cvtColor(blueCard, cv2.COLOR_BGR2HSV)
blueHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

wildCard = cv2.imread('./CardColors/wild.jpg')
hsv = cv2.cvtColor(wildCard, cv2.COLOR_BGR2HSV)
wildHist = cv2.calcHist([hsv],[0,1],None,[256,256],[0,256,0,256])

histogramArray = [redHist, yellowHist, greenHist, blueHist, wildHist]

zero = cv2.imread('./CardTypes/0.jpg',0)
one = cv2.imread('./CardTypes/1.jpg',0)
two = cv2.imread('./CardTypes/2.jpg',0)
three = cv2.imread('./CardTypes/3.jpg',0)
four = cv2.imread('./CardTypes/4.jpg',0)
five = cv2.imread('./CardTypes/5.jpg',0)
six = cv2.imread('./CardTypes/6.jpg',0)
seven = cv2.imread('./CardTypes/7.jpg',0)
eight = cv2.imread('./CardTypes/8.jpg',0)
nine = cv2.imread('./CardTypes/9.jpg',0)
reverse = cv2.imread('./CardTypes/reverse.jpg',0)
skip = cv2.imread('./CardTypes/skip.jpg',0)
draw2 = cv2.imread('./CardTypes/draw2.jpg',0)
draw4 = cv2.imread('./CardTypes/draw4.jpg',0)
wild = cv2.imread('./CardTypes/wil.jpg',0)

cardTypes = [zero, one, two, three, four, five,
			 six, seven, eight, nine, reverse,
			 skip, draw2, draw4, wild]

sift = cv2.xfeatures2d.SIFT_create()

typeFeatures = []


for x in range(0,15):
	kp2, des2 = sift.detectAndCompute(cardTypes[x], None)
	typeFeatures.append(kp2)
	typeFeatures.append(des2)
	if x==7:
		print "STILL LOADING......"
	if x==13:
		print "ALMOST THERE......."

# Will only run once.
cap = cv2.VideoCapture(0)
time.sleep(5)
print "camera open!"


def drawCard():
	# 1) physically pick up card
	# 2) analyze card
	# 3) in a the next available index in handOfCards[] (which corresponds to physical location),
	# 		store card color and type

	'''
											handOfCards
	index:		0			1			2			3			4			5			6		7
	ID:		card1Color	card1Type	card2Color	card2Type	card3Color	card3Type ...
	'''

	print("drawn lol")

def analyzeCard(frame):
	cardcolor = findColorMatch(frame)
	cardtype = findTypeMatch(frame)

	card = (cardcolor, cardtype)

	return card


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
		return "RED"
	elif histogramIndex == 1:
		return "YELLOW"
	elif histogramIndex == 2:
		return "GREEN"
	elif histogramIndex == 3:
		return "BLUE"
	elif histogramIndex == 4:
		return "WILD"

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

	return matchIndex

def main():
	while(True):
		if(cap.isOpened() == False):
			print("Error!")
			break

		ret, frame = cap.read()
		if(ret == True):
			#findColorMatch(frame)
			#findTypeMatch(frame)

			newCard = (findColorMatch(frame), findTypeMatch(frame))
			print "Active card is ", newCard

			for card in handOfCards:
				if card[0] == newCard[0]:
					'''
					play this card
					'''
					print "play your", card, "card!"
					break
				elif card[1] == newCard[1]:
					'''
					play this card
					'''
					print "play your", card, "card!"
					break

		cv2.imshow("Camera", frame)


		# You have 20 seconds to make your next move!
		key = cv2.waitKey(2500) & 0xFF

		if key == ord("q"):
			break
			

		

	cap.release()

if __name__ == '__main__':
	main()
