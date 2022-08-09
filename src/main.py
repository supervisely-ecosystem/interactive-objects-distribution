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
# table per page change default
# progress bar - checkbox ok, finished message, hide after success
# x/y axis title - linechart
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

# define all UI widgets here
project_info = sly.app.widgets.ProjectThumbnail(project)
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")
chart = sly.app.widgets.LineChart(
    title="Objects count distribution for every class",
    xaxis_type="category",
    xaxis_title="Number of objects",
    yaxis_title="Number of images",
)


iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)
iris.insert(loc=0, column="index", value=np.arange(len(iris)))
table = sly.app.widgets.Table(data=iris, width="100%")  # fixed_cols=1


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.LineChart.ClickedDataPoint):
    print(f"Line: {datapoint.series_name}")
    print(f"x = {datapoint.x}")
    print(f"y = {datapoint.y}")


@button.click
def calculate_stats():
    # "id", "dataset", "name (click)" , "width", "height", "objects", preview,

    # class name -> objects count (x) -> images count (y)
    chart = defaultdict(lambda: defaultdict(int))

    # class name -> objects count (x) -> {image_info, row}
    tables = defaultdict(lambda: defaultdict(lambda: {"infos": [], "rows": []}))

    # tables = defaultdict(lambda: defaultdict(lambda: {"infos": [], "rows": []}))
    # for obj_class in meta.obj_classes:
    #     obj_class: sly.ObjClass
    #     chart[obj_class.name] = defaultdict(lambda: defaultdict(int))
    #     tables[obj_class.name] = defaultdict(
    #         lambda: defaultdict(lambda: {"infos": [], "rows": []})
    #     )

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
                for class_name, objects_count in counters.items():
                    chart[class_name][objects_count] += 1
                    tables[class_name][objects_count]["infos"].append(image)
                    tables[class_name][objects_count]["rows"].append(
                        [
                            image.id,
                            dataset.name,
                            image.name,
                            len(ann.labels),
                            image.width,
                            image.height,
                        ]
                    )

    for name in ["maxim", "denis"]:
        total = 20
        with progress(message=f"Generating '{name}' chart...", total=total) as pbar:
            for i in range(total):
                time.sleep(0.1)
                pbar.update(1)
        x, y = generate_random_chart(random.randint(15, 30))
        chart.add_series(name, x, y)


@table.click
def show_image(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    print("Column name = ", datapoint.column_name)
    print("Cell value = ", datapoint.cell_value)
    print("Row = ", datapoint.row)


def generate_random_chart(n=30):
    x = list(range(n))
    y = np.random.randint(low=0, high=300, size=n).tolist()
    return x, y
