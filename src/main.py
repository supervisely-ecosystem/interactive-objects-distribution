import os
from dotenv import load_dotenv
import supervisely as sly
import time
from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = FastAPI()
sly.app.fastapi.init(app)

# app.mount("/sly", sly.app.fastapi.create())
# templates = sly.app.fastapi.Jinja2Templates(directory="templates")
# sly.app.fastapi.enable_hot_reload_on_debug(app)

from supervisely.app.widgets import ElementButton, SlyTqdm

progress = SlyTqdm(message="My progress")
button = ElementButton(text="Start")


@app.get("/")
async def read_index(request: Request):
    return sly.app.fastapi.Jinja2Templates().TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@button.add_route(app=app, route=ElementButton.Routes.BUTTON_CLICKED)
def count(
    state: sly.app.StateJson = Depends(sly.app.StateJson.from_request),
):
    total = 100
    pbar = progress(message="Downloading project...", total=total)
    for i in range(total):
        time.sleep(0.1)
        pbar.update(1)
    pbar.close()
