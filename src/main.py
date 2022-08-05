import os
from dotenv import load_dotenv
import supervisely as sly
from fastapi import FastAPI, Request, Depends


app = FastAPI()
app.mount("/sly", sly.app.fastapi.create())
templates = sly.app.fastapi.Jinja2Templates(directory="templates")
# sly.app.fastapi.enable_hot_reload_on_debug(app)


@app.get("/")
async def read_index(request: Request):
    template = templates.TemplateResponse("index.html", {"request": request})
    return template
