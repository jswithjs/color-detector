from colorthief import ColorThief
import pandas as pd

color_thief = ColorThief('pic1.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=10)
palette = color_thief.get_palette(color_count=100)

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

c = list(map(rgb_to_hex, palette))
v = list(map(hex_nearest_match, c))
print(v)