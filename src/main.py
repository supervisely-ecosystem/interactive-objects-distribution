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
            "smoothingWeight": 0.7,
            "groupKey": None,
            "showLegend": True,
            "decimalsInFloat": 6,
            "yaxisInterval": [0.00088, 0.0011],
            "xaxisDecimalsInFloat": 3,
        },
        "series": [
            {
                "name": "Line 1",
                "data": [
                    [0.08333333333333333, 0.001],
                    [0.16666666666666666, 0.001],
                    [0.25, 0.001],
                    [0.3333333333333333, 0.001],
                    [0.4166666666666667, 0.001],
                    [0.5, 0.001],
                    [0.5833333333333334, 0.001],
                    [0.6666666666666666, 0.001],
                    [0.75, 0.001],
                    [0.8333333333333334, 0.001],
                    [0.9166666666666666, 0.001],
                    [1, 0.001],
                    [1.0833333333333333, 0.00099],
                    [1.1666666666666667, 0.00099],
                    [1.25, 0.00099],
                    [1.3333333333333333, 0.00099],
                    [1.4166666666666667, 0.00099],
                    [1.5, 0.00099],
                    [1.5833333333333335, 0.00099],
                    [1.6666666666666665, 0.00099],
                    [1.75, 0.00099],
                    [1.8333333333333335, 0.00099],
                    [1.9166666666666665, 0.00099],
                    [2, 0.00099],
                    [2.0833333333333335, 0.0009801],
                    [2.1666666666666665, 0.0009801],
                    [2.25, 0.0009801],
                    [2.3333333333333335, 0.0009801],
                    [2.4166666666666665, 0.0009801],
                    [2.5, 0.0009801],
                    [2.5833333333333335, 0.0009801],
                    [2.6666666666666665, 0.0009801],
                    [2.75, 0.0009801],
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
