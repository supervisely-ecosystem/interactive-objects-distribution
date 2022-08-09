from collections import defaultdict
import os
from dotenv import load_dotenv
import supervisely as sly
import time
import numpy as np
import pandas as pd
import random

from supervisely.app.content import DataJson, StateJson

# TODO:
# from supervisely.app.fastapi import available_after_shutdown - auto in init
# table - fixed_cols test
# table - image name clickable + icon
# table - preview column
# GridGallery - replace image
# line chart - yaxis_autorescale=False

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()
app = sly.Application()

project_id = int(os.environ["modal.state.slyProjectId"])
project = api.project.get_info_by_id(project_id)
meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
if len(meta.obj_classes) == 0:
    raise ValueError("App finished: project does not have classes")
table_columns = ["id", "image", "dataset", "labels", "width", "height"]
tables_rows = None
stats = None


# define all UI widgets here
project_info = sly.app.widgets.ProjectThumbnail(project)
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")
chart = sly.app.widgets.LineChart(
    title="Objects count distribution for every class",
    xaxis_type="category",
    xaxis_title="Number of objects",
    yaxis_title="Number of images",
    height=350,
)
table = sly.app.widgets.Table(data=None, width="100%")  # fixed_cols=1
preview = sly.app.widgets.GridGallery(1)


@button.click
def calculate_stats():
    global stats, tables_rows
    # class name -> objects count (x) -> images count (y)
    stats = defaultdict(lambda: defaultdict(int))

    # class name -> objects count (x) -> {image_info, row}
    # row -> "id", "dataset", "name (click)" , "width", "height", "objects", preview
    tables_rows = defaultdict(lambda: defaultdict(lambda: {"infos": [], "rows": []}))

    max_x = 1
    with progress(message=f"Processing images...", total=project.items_count) as pbar:
        for dataset in api.dataset.get_list(project.id):
            images = api.image.get_list(dataset.id)
            for batch in sly.batched(images):
                batch_ids = [image.id for image in batch]
                annotations = api.annotation.download_json_batch(dataset.id, batch_ids)
                for image, ann_json in zip(batch, annotations):
                    ann = sly.Annotation.from_json(ann_json, meta)
                    counters = defaultdict(int)
                    for label in ann.labels:
                        counters[label.obj_class.name] += 1
                    for obj_class in meta.obj_classes:
                        class_name = obj_class.name
                        objects_count = counters[class_name]
                        stats[class_name][objects_count] += 1
                        max_x = max(max_x, objects_count)
                        tables_rows[class_name][objects_count]["infos"].append(image)
                        tables_rows[class_name][objects_count]["rows"].append(
                            [
                                image.id,
                                image.name,
                                dataset.name,
                                len(ann.labels),
                                image.width,
                                image.height,
                            ]
                        )
                    pbar.update(1)

    for class_name, d in stats.items():
        x = list(range(max_x + 1))
        y = [0] * len(x)
        for px, py in d.items():
            y[px] = py
        # x, y = list(d.keys()), list(d.values())
        chart.add_series(class_name, x, y)


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.LineChart.ClickedDataPoint):
    print(f"Line: {datapoint.series_name}")
    print(f"x = {datapoint.x}")
    print(f"y = {datapoint.y}")

    class_name = datapoint.series_name
    objects_count = datapoint.x
    images_count = datapoint.y

    rows = tables_rows[class_name][objects_count]["rows"]
    if len(rows) != images_count:
        raise ValueError("num rows in table != num images in chart")
    df = pd.DataFrame(rows, columns=table_columns)
    table.read_pandas(df)


@table.click
def show_image(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    print("Column name = ", datapoint.column_name)
    print("Cell value = ", datapoint.cell_value)
    print("Row = ", datapoint.row)

    image_id = datapoint.row["id"]
    image = api.image.get_info_by_id(image_id)
    ann_json = api.annotation.download_json(image_id)
    ann = sly.Annotation.from_json(ann_json, meta)
    preview.append(image.preview_url, ann, image.name)

    # df = pd.DataFrame(data, columns=["Name", "Age"])
