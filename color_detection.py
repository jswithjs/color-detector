from pprint import pprint
import cv2
import numpy as np
import pandas as pd
from multiprocessing import Process, Array

df = pd.read_csv(
		'colors.csv',
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None)
results = np.zeros(len(df))
df_nodes = df.to_numpy()
nodes = df_nodes[..., (3, 4, 5)]

img = cv2.imread('pic1.jpg')
img = img.reshape((img.shape[0] * img.shape[1], 3))

def get_color_name_optimized_v5(RGB):
	index = np.sum(np.power(nodes - RGB, 2), axis = 1)
	c = np.argmin(index)
	return c

def get_color_final(img):
	results[get_color_name_optimized_v5([0, 0, 0])] = np.count_nonzero(img == [0, 0, 0])
	img = img[img != [0, 0, 0]]
	while len(img) != 0:
		now = img[0]
		results[get_color_name_optimized_v5(now)] += np.count_nonzero(img == now)
		img = img[img != now]
