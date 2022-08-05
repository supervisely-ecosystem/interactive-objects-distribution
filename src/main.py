import os
from dotenv import load_dotenv
import supervisely as sly
import time

from fastapi import FastAPI, Request, Depends
from supervisely.app.fastapi import available_after_shutdown

# "GET /app/widgets/element_button/style.css HTTP/1.1" 304 Not Modified
# "GET /app/widgets/sly_tqdm/style.css HTTP/1.1" 304 Not Modified
# method arguments (btn click) - state, context - hide
# question - notification box DataJson()[self.widget_id]['title'] = self._title, remove widget_id???
# head -> title в index.html ставить автоматом
# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# altair visualizations
# "GET /app/widgets/sly_tqdm/style.css HTTP/1.1" 304 Not Modified

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
