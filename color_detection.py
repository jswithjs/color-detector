import cv2
import pandas as pd
import rgbtocmyk

df = pd.read_csv(
		'colors.csv', 
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None
	)

img = cv2.imread('pic1.jpg')
img = cv2.resize(img, (800,600))

clicked = False
r = g = b = xpos = ypos = 0

def get_color_name(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']
	return cname

def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
	cv2.imshow('image', img)
	(c, m, y, black) = rgbtocmyk.RGBtoCMYK(r, g, b)

	if clicked:
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

		text = get_color_name(r,g,b) + ' C=' + str(c) + ' M=' + str(m) + ' Y=' + str(y) + ' K=' + str(black)
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		print(r + g + b)
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
