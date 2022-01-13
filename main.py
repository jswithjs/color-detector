from fastapi import FastAPI, Form, File
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import cv2

app = FastAPI()

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color

async def prep_image(raw_img):
    img = np.frombuffer(raw_img, dtype = np.uint8)
    img = cv2.imdecode(img, flags=cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    modified_img = cv2.resize(img, (900, 600), interpolation = cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
    return modified_img

@app.post("/")
async def color_analysis(img: bytes = File(...), n = Form(...)):
    img = await prep_image(img)
    n   = int(n)
    clf = KMeans(n_clusters = n)
    color_labels_l = clf.fit_predict(img)
    center_colors  = clf.cluster_centers_
    counts = Counter(color_labels_l)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]

    ret = {}
    for i in range(0, n):
        c = hex_colors[i]
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
