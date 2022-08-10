import os
from dotenv import load_dotenv
import supervisely as sly
import src.stats as stats

# TODO:
# from supervisely.app.fastapi import available_after_shutdown - auto in init
# grid gallery - empty gallery message
# label - click on XXX to see YYY
# label - you clicked XXX and it is YYY
# hide button after sucess

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()
app = sly.Application()

# variables
project_id = int(os.environ["modal.state.slyProjectId"])
project = api.project.get_info_by_id(project_id)
meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
stats.init(project, meta)

# all UI widgets
project_info = sly.app.widgets.ProjectThumbnail(project)
progress = sly.app.widgets.Progress()
button = sly.app.widgets.Button(text="Start", icon="zmdi zmdi-play")
chart = sly.app.widgets.LineChart(
    title="Objects count distribution for every class",
    xaxis_type="category",
    xaxis_title="Number of objects",
    yaxis_title="Number of images",
)
table = sly.app.widgets.Table(fixed_cols=1, width="100%")
labeled_image = sly.app.widgets.LabeledImage()


@button.click
def calculate_stats():
    with progress(message=f"Processing images...", total=project.items_count) as pbar:
        for dataset in api.dataset.get_list(project.id):
            images = api.image.get_list(dataset.id)
            for batch in sly.batched(images):
                batch_ids = [image.id for image in batch]
                annotations = api.annotation.download_json_batch(dataset.id, batch_ids)
                for image, ann_json in zip(batch, annotations):
                    ann = sly.Annotation.from_json(ann_json, meta)
                    stats.increment(dataset, image, ann)
                    pbar.update(1)

    for class_name, x, y in stats.get_series():
        chart.add_series(class_name, x, y)


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.LineChart.ClickedDataPoint):
    df = stats.get_table_data(cls_name=datapoint.series_name, obj_count=datapoint.x)
    table.read_pandas(df)


@table.click
def show_image(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    labeled_image.loading = True
    image_id = datapoint.row["id"]
    image = api.image.get_info_by_id(image_id)
    ann_json = api.annotation.download_json(image_id)
    ann = sly.Annotation.from_json(ann_json, meta)
    labeled_image.set(title=image.name, image_url=image.preview_url, ann=ann)
    labeled_image.loading = False
