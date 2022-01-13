from fastapi import FastAPI, Form
from collections import Counter
from base64 import b64decode
import numpy as np
from sklearn.cluster import KMeans
import cv2
import pandas as pd

app = FastAPI()

df = pd.read_csv(
		'colors.csv',
		names = ['color', 'color_name', 'hex', 'R', 'G', 'B'],
		header=None)

df_nodes   =  df.to_numpy()
names      =  df_nodes[..., 1]
hex_names  =  df_nodes[..., 2]
name_hex   =  df_nodes[..., 2].tolist()

def hex_nearest_match(h):
    if h in hex_names:
        return h
    
    h_I = int(h[1: ], 16)
    
    lb = hex_names[hex_names < h]
    ub = hex_names[hex_names > h]
    
    if lb.shape[0]:
        res =  ub[0]
    elif ub.shape[0]:
        res =  lb[-1]
    else:    
        ub_I = int(ub[1: ], 16)
        lb_I = int(lb[1: ], 16)
        if h_I - lb_I < ub_I - h_I:
            res =  lb
        else:
            res = ub
    
    return names[name_hex.index(res)]

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color

async def prep_image(raw_img):
    img = b64decode(raw_img)
    img = np.frombuffer(img, dtype = np.uint8)
    img = cv2.imdecode(img, flags=cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    modified_img = cv2.resize(img, (900, 600), interpolation = cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
    return modified_img

@app.post("/")
async def color_analysis(img = Form(...), n = Form(...)):
    img = await prep_image(img)
    n   = int(n)
    clf = KMeans(n_clusters = n)
    color_labels_l = clf.fit_predict(img)
    center_colors  = clf.cluster_centers_
    counts = Counter(color_labels_l)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    hex_color_names = list(map(hex_nearest_match, hex_colors))

    ret = {}
    for i in range(0, n):
        c = hex_color_names[i]
        if i in ret:
            ret[c] += round((counts[i] * 100) / img.shape[0], 2)
        else:
            ret[c] = round((counts[i] * 100) / img.shape[0], 2)
    return {
        "status": 1,
        "result": ret
    }

@app.get("/")
async def home():
    return { "server": "up and Running!" }