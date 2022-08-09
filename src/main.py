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

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

project_id = int(os.environ["modal.state.slyProjectId"])
api = sly.Api()
project = api.project.get_info_by_id(project_id)

app = sly.Application()

# define all UI widgets here
project_info = sly.app.widgets.ProjectThumbnail(project)
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")
chart = sly.app.widgets.LineChart(title="Max vs Denis", xaxis_type="category")


iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)
iris.insert(loc=0, column="index", value=np.arange(len(iris)))
table = sly.app.widgets.Table(data=iris, fixed_cols=1)


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.LineChart.ClickedDataPoint):
    print(f"Line: {datapoint.series_name}")
    print(f"x = {datapoint.x}")
    print(f"y = {datapoint.y}")


@button.click
def calculate_stats():
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
