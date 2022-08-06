import os
from dotenv import load_dotenv
import supervisely as sly
import time

from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# sly.logger.debug("XXX") doesnt work
# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# altair visualizations
# SlyTqdm -> progress / TQDM???
# sly.timeit не работает

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = sly.Application()
progress = sly.app.widgets.SlyTqdm()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")


@button.click
def count():
    total = 50
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
