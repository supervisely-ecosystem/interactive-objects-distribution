import os
from dotenv import load_dotenv
import supervisely as sly
import time
import json
import pandas as pd
import plotly.express as px

# from supervisely.app.fastapi import available_after_shutdown


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

# df = px.data.stocks()
# fig = px.line(df, x="date", y="GOOG")
data = sly.app.DataJson()
# data["chart"] = json.loads(fig.to_json())

x = {
    "example2": {
        "options": {
            "title": "Small values",
            "groupKey": None,
            "showLegend": True,
        },
        "series": [
            {
                "name": "Line 1",
                "data": [
                    [1, 10],
                    [2, 20],
                    [3, 30],
                    [4, 40],
                    [5, 50],
                    [6, 60],
                    [7, 70],
                    [8, 80],
                    [9, 90],
                ],
            }
        ],
    }
}


data["example2"] = x["example2"]


@button.click
def count():
    total = 20
    with progress(message="Some processing...", total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)
