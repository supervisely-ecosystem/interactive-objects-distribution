import os
from dotenv import load_dotenv
import supervisely as sly
import time
import json
import pandas as pd
import numpy as np

from supervisely.app.content import StateJson

# from supervisely.app.fastapi import available_after_shutdown
# post method not found modal window
# apex chart - broken after zoom
# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# put point after click?

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

project_id = int(os.environ["modal.state.slyProjectId"])
api = sly.Api()
project = api.project.get_info_by_id(project_id)

# define all UI widgets here
app = sly.Application()
project_info = sly.app.widgets.ProjectThumbnail(project)
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")


size1 = 10
x1 = list(range(size1))
y1 = np.random.randint(low=10, high=148, size=size1).tolist()
s1 = [{"x": x, "y": y} for x, y in zip(x1, y1)]

size2 = 30
x2 = list(range(size2))
y2 = np.random.randint(low=0, high=300, size=size2).tolist()
s2 = [{"x": x, "y": y} for x, y in zip(x2, y2)]

chart = sly.app.widgets.LineChart(
    title="Max vs Denis",
    series=[{"name": "Max", "data": s1}, {"name": "Denis", "data": s2}],
    xaxis_type="category",
)


@chart.click
def refresh_images_table():
    print("refresh_images_table")


@button.click
def calculate_stats():
    StateJson()["fdsfd"]
    stats = {}
    # for dataset in api.dataset.get_list(project.id):
    #     images = api.image.get_list(dataset.id)
    #     for batch in sly.batched(images):
    #         image_ids = [image.id for image in batch]
    #         annotations = api.annotation.download_json_batch(dataset.id, image_ids)
    #         for ann_json in annotations:

    total = 20
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)

    return stats
