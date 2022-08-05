import os
from dotenv import load_dotenv
import supervisely as sly
import time
from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# index.html - hide
# app.get("/") - hide
# app = FastAPI() - remove
# app = sly.app.fastapi.init()
# @button.click(app) -> @button.click()
# hide widgets init app object somewhere inside - app singletone
# method arguments (btn click) - state, context - hide
# api - one time init (session owner, !!!session user!!)
# question - notification box DataJson()[self.widget_id]['title'] = self._title, remove widget_id???
# head -> title в index.html ставить автоматом
# версии JS скриптов в index.html - суем в SDK внутрь - привязываемся к версии pySDK
# for convenient debug, has no effect in production
# Jinja2Templates - прячем
# storage_image_url - server address join using flag
# app_mode -> "running_on": "Supervisely", or "localhost"

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = FastAPI()
sly.app.fastapi.init(app)

progress = sly.app.widgets.SlyTqdm()
button = sly.app.widgets.ElementButton(text="Start")


@app.get("/")
async def read_index(request: Request):
    return sly.app.fastapi.Jinja2Templates().TemplateResponse(
        "index.html", {"request": request}
    )


@button.click(app)
def count(
    state: sly.app.StateJson = Depends(sly.app.StateJson.from_request),
):
    total = 100
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
