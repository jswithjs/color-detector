import cv2
import rgbtocmyk

def process__sample_image(img_name):
	img = cv2.imread(img_name)
	img = cv2.resize(img, (800,600))
	IMG = rgbtocmyk.rImage(img)
	while True:
		cv2.imshow('image', img)
		cv2.rectangle(img, (20,20), (480,60), (0, 0, 0), -1)

		text = 'C: {C} M: {M}, Y: {Y}, K:{K}'.format_map(IMG)
		cv2.putText(
			img, 
			text, 
			(50, 50), 
			2, 0.8,
			(255,255,255), 2,
			cv2.LINE_AA)

		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	for i in '1', '2', '3': 
		process__sample_image('pic' + i + '.jpg')