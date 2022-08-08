import os
from dotenv import load_dotenv
import supervisely as sly
import time
import pandas as pd

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
print(project)
print(project.reference_image_url)
print(project.image_preview_url)

sly.app.StateJson()["abc"] = {}

app = sly.Application()
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")
project_info = sly.app.widgets.ProjectThumbnail(project)


import json

data = sly.app.DataJson()
data["output1"] = {"a": 123}
data["example1"] = json.loads(
    '{"series":[{"name":"Desktops","data":[10,41,35,51,49,62,69,91,148]}],"chartOptions":{"chart":{"height":350,"type":"line","zoom":{"enabled":false}},"dataLabels":{"enabled":false},"stroke":{"curve":"straight"},"title":{"text":"Product Trends by Month","align":"left"},"grid":{"row":{"colors":["#f3f3f3","transparent"],"opacity":0.5}},"xaxis":{"categories":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"]}}}'
)

data["output2"] = {"a": 123}
data["example2"] = json.loads(
    '{"series":[{"name":"Net Profit","data":[44,55,57,56,61,58,63,60,66]},{"name":"Revenue","data":[76,85,101,98,87,105,91,114,94]},{"name":"Free Cash Flow","data":[35,41,36,26,45,48,52,53,41]}],"chartOptions":{"chart":{"type":"bar","height":350},"plotOptions":{"bar":{"horizontal":false,"columnWidth":"55%","endingShape":"rounded"}},"dataLabels":{"enabled":false},"stroke":{"show":true,"width":2,"colors":["transparent"]},"xaxis":{"categories":["Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct"]},"yaxis":{"title":{"text":"$ (thousands)"}},"fill":{"opacity":1}}}'
)


@button.click
def count():
    total = 20
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
