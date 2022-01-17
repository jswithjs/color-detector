from PIL import Image
import io
from lib import get_palette, get_color
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color

async def process(image_buffer):
    IMAGE  = Image.open(io.BytesIO(image_buffer))
    ACCURACY = 0.05
    _, p_map = get_palette(IMAGE, 0xff, 10)
    
    ret = {}
    for i in p_map.vboxes.contents:
        color_name = rgb_to_hex(i['color'])
        ret[color_name] = i['vbox'].count
    
    FINAL = sum(ret.values())
    n_ret = {}
    for i in ret:
        tmp = round((ret[i] / FINAL) * 100, 2)
        if tmp > ACCURACY:
            print(tmp)
            n_ret[i] = tmp
    return n_ret

app = FastAPI()
app.add_middleware(
    CORSMiddleware
    , allow_origins=["*"])

@app.post('/')
async def home(img: bytes = File(...)):
    try:
        c = await process(img)
        return {
            "Status": 1
            , "data": c
        }
    except Exception as e:
        return {"Error": str(e)}

@app.get("/")
async def home():
    return { "server": "up and Running!" }