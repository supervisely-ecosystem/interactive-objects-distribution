import os
from dotenv import load_dotenv
import supervisely as sly
import time
import json
import pandas as pd
import numpy as np

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

data = sly.app.DataJson()
data["output1"] = {"a": 123}

size1 = 10
x1 = list(range(size1))
y1 = np.random.randint(low=10, high=148, size=size1).tolist()
s1 = [{"x": x, "y": y} for x, y in zip(x1, y1)]

size2 = 30
x2 = list(range(size2))
y2 = np.random.randint(low=0, high=300, size=size2).tolist()
s2 = [{"x": x, "y": y} for x, y in zip(x2, y2)]


# data["example1"] = {
#     "series": [{"name": "Desktops", "data": y1}],
#     "chartOptions": {
#         "chart": {"height": 350, "type": "line", "zoom": {"enabled": False}},
#         "dataLabels": {"enabled": False},
#         "stroke": {"curve": "straight"},
#         "title": {"text": "Product Trends by Month", "align": "left"},
#         "grid": {"row": {"colors": ["#f3f3f3", "transparent"], "opacity": 0.5}},
#         "xaxis": {
#             "categories": [
#                 "Jan",
#                 "Feb",
#                 "Mar",
#                 "Apr",
#                 "May",
#                 "Jun",
#                 "Jul",
#                 "Aug",
#                 "Sep",
#             ]
#         },
#     },
# }

print(y1)
data["example1"] = {
    "series": [{"name": "Max", "data": s1}, {"name": "Denis", "data": s2}],
    "chartOptions": {
        "chart": {"type": "line", "zoom": {"enabled": False}},
        "dataLabels": {"enabled": False},
        # "stroke": {"curve": "straight"},
        "stroke": {"curve": "smooth", "width": 2},
        "title": {"text": "Product Trends by Month", "align": "left"},
        "grid": {"row": {"colors": ["#f3f3f3", "transparent"], "opacity": 0.5}},
        "xaxis": {"type": "category"},
    },
}

# data["example1"] = json.loads(
#     '{"series":[{"name":"Desktops","data":[10,41,35,51,49,62,69,91,148]}],"chartOptions":{"chart":{"height":350,"type":"line","zoom":{"enabled":false}},"dataLabels":{"enabled":false},"stroke":{"curve":"straight"},"title":{"text":"Product Trends by Month","align":"left"},"grid":{"row":{"colors":["#f3f3f3","transparent"],"opacity":0.5}},"xaxis":{"categories":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"]}}}'
# )

# print(json.dumps(data["example1"], indent=4))

data["output2"] = {"a": 123}
data["example2"] = json.loads(
    '{"series":[{"name":"Net Profit","data":[44,55,57,56,61,58,63,60,66]},{"name":"Revenue","data":[76,85,101,98,87,105,91,114,94]},{"name":"Free Cash Flow","data":[35,41,36,26,45,48,52,53,41]}],"chartOptions":{"chart":{"type":"bar","height":350},"plotOptions":{"bar":{"horizontal":false,"columnWidth":"55%","endingShape":"rounded"}},"dataLabels":{"enabled":false},"stroke":{"show":true,"width":2,"colors":["transparent"]},"xaxis":{"categories":["Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct"]},"yaxis":{"title":{"text":"$ (thousands)"}},"fill":{"opacity":1}}}'
)


@button.click
def calculate_stats():
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
