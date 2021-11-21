from pprint import pprint
import cv2
import numpy as np
import pandas as pd
from multiprocessing import Pool

df = pd.read_csv(
		'colors.csv',
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None)
results = np.zeros(len(df), dtype=int)
df_nodes = df.to_numpy()
nodes = df_nodes[..., (3, 4, 5)]

img = cv2.imread('pic1.jpg')
img = cv2.resize(img, (800,600))
img = img.reshape((800 * 600, 3))

def get_color_name_optimized_v5(RGB):
	global results
	index = np.sum(np.power(nodes - RGB, 2), axis = 1)
	c = np.argmin(index)
	results[c] += 1
	return c

def get_color_statistics_v2(img):
	with Pool(5) as p:
		c = p.map(get_color_name_optimized_v5, img[0:16000])
	pprint(results[results != 0])
	