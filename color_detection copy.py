import cv2
import numpy as np
import pandas as pd

df = pd.read_csv(
		'colors.csv',
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None)


df_nodes = df.to_numpy()
nodes = df_nodes[..., (3, 4, 5)]
names = df_nodes[..., 1]

img = cv2.imread('pic1.jpg')
img = cv2.resize(img, (800, 600))
img = img.reshape((img.shape[0] * img.shape[1], img.shape[2]))

results = np.zeros(len(df))
def get_name(RGB):
	index = np.sum(np.power(nodes - RGB, 2), axis = 1)
	c = np.argmin(index)
	return c

ncount = lambda x: np.count_nonzero(x)

def get_color_final(img):
	black = [0, 0, 0]

	results[get_name(black)] += ncount(img == black)
	img = img[img != black]
	
	while len(img) != 0:
		now = img[0]
		results[get_name(now)] += ncount(img == now)
		img = img[img != now]

	return results

r = get_color_final(img)
print(r)
