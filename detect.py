from collections import Counter
from sklearn.cluster import KMeans
import numpy as np
import cv2

image = cv2.imread('pic1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color

def prep_image(raw_img):
    modified_img = cv2.resize(raw_img, (900, 600), interpolation = cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
    return modified_img

def color_analysis(img, n):
    clf = KMeans(n_clusters = n)
    color_labels_l = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels_l)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]    
    return { hex_colors[a]: counts[a] for a in range(0, n) }

modified_image = prep_image(image)
a = color_analysis(modified_image, 10)
print(a)
