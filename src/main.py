import os
from dotenv import load_dotenv
import supervisely as sly
import time
from supervisely.app.fastapi import available_after_shutdown

# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# altair visualizations
# api inti print exception + link to documentation

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

app = sly.Application()
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")

api = sly.Api()
api = sly.Api.from_env()


@button.click
def count():
    total = 20
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
