import os
from dotenv import load_dotenv
import supervisely as sly
import time
import numpy as np

# from supervisely.app.fastapi import available_after_shutdown
# post method not found modal window
# storage_image_url - server address join using flag
# available_after_shutdown hiddend - auto in init
# put point after click?
# add_event_handler - maybe remove?

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


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.LineChart.ClickedDataPoint):
    print(f"User clicked {datapoint.series_name}, x = {datapoint.x}, y = {datapoint.y}")


@button.click
def calculate_stats():
    total = 20
    with progress(message="Generating first chart...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)

    name = "Max"
    x, y = generate_random_chart(15)
    chart.add_series(name, x, y)

    total = 30
    with progress(message="Generating second chart...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)

    name = "Denis"
    x, y = generate_random_chart(40)
    chart.add_series(name, x, y)


def generate_random_chart(n=30):
    x = list(range(n))
    y = np.random.randint(low=0, high=300, size=n).tolist()
    return x, y
