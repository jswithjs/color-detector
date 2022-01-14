from PIL import Image
import io
from lib import get_palette, get_color
from fastapi import FastAPI, File, Form
from fastapi.middleware.cors import CORSMiddleware

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color

async def process(image_buffer, n): 
    IMAGE  = Image.open(io.BytesIO(image_buffer))
    IMAGE  = IMAGE.resize((1280, 720))
    if n == 1:
        return {
            rgb_to_hex(get_color(IMAGE)): 100
        }
    _, p_map = get_palette(IMAGE, n, 10)
    
    ret = {}
    for i in p_map.vboxes.contents:
        color_name = rgb_to_hex(i['color'])
        ret[color_name] = i['vbox'].count
    
    FINAL = sum(ret.values())
    for i in ret:
        ret[i] = round((ret[i] / FINAL) * 100, 2)
    return ret

app = FastAPI()
app.add_middleware(
    CORSMiddleware
    , allow_origins=["*"])


@app.post('/')
async def home(img: bytes = File(...), n: int = Form(...)):
    try:
        c = await process(img, n)
        return {
            "Status": 1
            , "data": c
        }
    except Exception as e:
        return {"Error": str(e)}

@app.get("/")
async def home():
    return { "server": "up and Running!" }
