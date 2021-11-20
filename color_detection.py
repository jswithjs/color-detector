import cv2
import numpy as np
from pprint import pprint
import pandas as pd
from multiprocessing import Pool, Process, Queue
from functools import lru_cache
#import rgbtocmyk

df = pd.read_csv(
		'colors.csv', 
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None
	)

img = cv2.imread('pic1.jpg')
img = cv2.resize(img, (800,600))

@lru_cache(128)
def build_circle_v2(r, g, b, rad):
	radR = lambda a: np.power(a[0] - a[1], 2)
	ret = []
	ret.append([df.R, r])
	ret.append([df.G, g])
	ret.append([df.B, b])
	ret = sum(list(map(radR, ret)))
	return df[ret < np.power(rad, 2)]

def build_circle(r, g, b, rad):
	ret  = (df.R - r)**2
	ret += (df.G - g)**2
	ret += (df.B - b)**2
	return df[ret < (rad * rad)]

def get_color_name_optimized(RGB, _init_c = 1):
	r, g, b = RGB
	_init = 1
	c = build_circle(r, g, b, _init)
	while c.empty:
		_init += _init_c
		c = build_circle(r, g, b, _init)
	
	if _init_c < 0.125:
		return c

	if len(c) == 1:
		return c.color_name.values[0]
	return get_color_name_optimized(RGB, _init_c = _init_c / 2)


def get_color_name_optimized_v2(RGB):
	r, g, b = RGB
	_init = 1
	c = build_circle_v2(r, g, b, _init)
	while c.empty:
		_init += 0.5
		c = build_circle_v2(r, g, b, _init)

	if len(c) == 1 or True:
		return c.color_name.values[0]

def get_color_name_optimized_v2_1(RGB, q):
	r, g, b = RGB
	_init = 1
	c = build_circle_v2(r, g, b, _init)
	while c.empty:
		_init += 0.5
		c = build_circle_v2(r, g, b, _init)

	q.put(c.color_name.values[0])


def get_color_name_optimized_v3(RGB_list):
	mq = []
	for i in range(12):
		r1 = i * 50
		r2 = r1 + 50
		m = Queue()
		p = Process(
			target=get_color_name_optimized_v2_1
			, args=(RGB_list, m)).start()
		mq.append(m)
	c = []
	for i in mq:
		c = c + i.get()
	return c


def get_color_statistics(img):
	c = {}
	for i in img:
		for j in i:
			name = get_color_name_optimized_v2(j)
			if name in c:
				c[name] += 1
			else:
				c[name] = 1
	return c

def get_color_statistics_v2(img):
	c = {}
	p = Pool(20)
	for i in img:
		print(p.map(get_color_name_optimized_v2, i))
	return None


def get_color_name(RGB, df=df):
	[R, G, B] = RGB
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']
	return cname

def get_result(d, shape):
	for i in d:
		d[i] = d[i] / shape
	return d

# d = get_color_statistics(img)
# shape = img.shape[0] * img.shape[1]
# res = get_result(d, shape)
# pprint(res)

# cv2.namedWindow('image')
# cv2.setMouseCallback('image', draw_function)

# while True:
# 	cv2.imshow('image', img)
# 	(c, m, y, black) = rgbtocmyk.RGBtoCMYK(r, g, b)

# 	if clicked:
# 		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

# 		text = get_color_name(r,g,b) + ' C=' + str(c) + ' M=' + str(m) + ' Y=' + str(y) + ' K=' + str(black)
# 		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

# 		print(r + g + b)
# 		if r+g+b >=600:
# 			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

# 	if cv2.waitKey(20) & 0xFF == ord('q'):
# 		break

# cv2.destroyAllWindows()