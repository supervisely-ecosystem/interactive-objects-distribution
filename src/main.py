import os
from dotenv import load_dotenv
import supervisely as sly
import time

from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# altair visualizations

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = sly.Application()
progress = sly.app.widgets.SlyTqdm()
button = sly.app.widgets.ElementButton(text="Start")


@button.click()
def count(
    state: sly.app.StateJson = Depends(sly.app.StateJson.from_request),
):
    total = 100
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
