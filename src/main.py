import os
from dotenv import load_dotenv
import supervisely as sly
from supervisely.app.widgets import (
    Container,
    Card,
    Button,
    Text,
    Progress,
    ProjectThumbnail,
    HeatmapChart,
)
import src.stats as stats

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()


# get project info from server
project_id = sly.env.project_id()
project = api.project.get_info_by_id(project_id)
meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
stats.init(project, meta)

############## initialize widgets and gui layout ##############

# input project
project_info = ProjectThumbnail(project)
input_card = Card(
    title="Input project", description="All labels will be used in stats", content=project_info
)

# interactive heatmap chart
progress = Progress()
button = Button(text="Calculate stats", icon="zmdi zmdi-play")
chart = HeatmapChart(
    title="Objects on images - distribution for every class",
    xaxis_title="Number of objects on image",
    color_range="row",
    tooltip="There are {y} images with {x} objects of class {series_name}",
)
chart.hide()
heatmap_card = Card(
    title="1️⃣ Interactive chart",
    description="👉 Click on chart datapoint to show table with corresponding images",
    content=Container([progress, button, chart]),
)

# interactive images table with preview gallery
chart_click_info = sly.app.widgets.NotificationBox()
table = sly.app.widgets.Table(fixed_cols=1, width="100%")
table_card = Card(
    title="2️⃣ Images table",
    description="👉 Click on table row to preview image",
    content=Container([chart_click_info, table]),
)
labeled_image = sly.app.widgets.LabeledImage()
preview_card = Card(
    title="3️⃣ Image preview",
    description="👉 Click table cell to preview image with labels",
    content=labeled_image,
)
image_exploration = Container(
    widgets=[table_card, preview_card], direction="horizontal", gap=15, fractions=[1, 1]
)

app = sly.Application(
    layout=Container(
        widgets=[input_card, heatmap_card, image_exploration],
        direction="vertical",
        gap=15,
    )
)


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

    lines = []
    for class_name, x, y in stats.get_series():
        # skip images without objects (x = 0)
        lines.append({"name": class_name, "x": x, "y": y})
    chart.add_series_batch(lines)

    button.hide()
    chart.show()


@chart.click
def refresh_images_table(datapoint: sly.app.widgets.HeatmapChart.ClickedDataPoint):
    table.loading = True
    labeled_image.clean_up()
    df = stats.get_table_data(cls_name=datapoint.series_name, obj_count=datapoint.x)
    table.read_pandas(df)
    chart_click_info.set(
        title="Table for clicked chart datapoint",
        description=f"Images that have at least {datapoint.x} object(s) of class {datapoint.series_name}",
    )
    table.loading = False


@table.click
def show_image(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    if datapoint.button_name is None:
        return
    labeled_image.loading = True
    image_id = datapoint.row["id"]
    image = api.image.get_info_by_id(image_id)
    ann_json = api.annotation.download_json(image_id)
    ann = sly.Annotation.from_json(ann_json, meta)
    labeled_image.set(title=image.name, image_url=image.preview_url, ann=ann)
    labeled_image.loading = False
