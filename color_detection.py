from multiprocessing import Pool
from collections import Counter
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
hex_names = df_nodes[..., 2]

img = cv2.imread('pic1.jpg')
img = cv2.resize(img, (800, 600))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img.reshape((img.shape[0] * img.shape[1], 3))

def rgb_to_hex(rgb_color):
	hex_color = "#"
	for i in rgb_color:
		i = int(i)
		hex_color += ("{:02x}".format(i))
	return hex_color

def ordl(s):
	return int(s[1: ], 16)

def hex_nearest_match(h):
	if h in hex_names:
		return h
	
	h_I = ordl(h)
	lb = hex_names[hex_names < h][-1]
	lb_I = ordl(lb)
	ub = hex_names[hex_names > h][0]
	ub_I = ordl(ub)
	if h_I - lb_I < ub_I - h_I:
		return lb
	return ub

def gname(x):
	hn = list(hex_names)
	return names[hn.index(x)]

res = list(map(rgb_to_hex, img))
with Pool(100) as p:
	resc = list(map(hex_nearest_match, res))

c = Counter(resc)
r = {
	gname(a): b 
	for a, b in c.most_common()}