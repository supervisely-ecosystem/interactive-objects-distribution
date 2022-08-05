import os
from dotenv import load_dotenv
import supervisely as sly
from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = FastAPI()
app.mount("/sly", sly.app.fastapi.create())
templates = sly.app.fastapi.Jinja2Templates(directory="templates")
# sly.app.fastapi.enable_hot_reload_on_debug(app)

from supervisely.app.widgets import ElementButton, SlyTqdm

progress = SlyTqdm(message="My progress")
button = ElementButton(text="Start")


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
