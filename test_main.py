from main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

t_client = TestClient(app)

def test_read_main():
    get_response = t_client.get("/")
    assert get_response.status_code == 200
    assert get_response.json() == { "server": "up and Running!" }

    file = "sample.jpg"
    f_bytes = open(file, "rb")
    post_response = t_client.post("/", files={"img": ("Wallpaper.jpg", f_bytes, "image/jpeg")})
    assert post_response.status_code == 200
    
    obj_res = post_response.json()
    obj_dat = obj_res['data'].values()
    assert obj_res['status'] == 1
    assert all([i > 0.05 for i in obj_dat])
