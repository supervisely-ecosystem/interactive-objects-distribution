from collections import defaultdict
import pandas as pd
import supervisely as sly


team: sly.TeamInfo = None
workspace: sly.WorkspaceInfo = None
project: sly.ProjectInfo = None
meta: sly.ProjectMeta = None

table_columns = ["id", "image", "dataset", "labels", "width", "height", "preview"]
# class name -> objects count (x) -> (images count - y) and (table rows)
stats = defaultdict(lambda: defaultdict(lambda: {"images_count": 0, "table_rows": []}))
max_x = 1


def init(project_info: sly.ProjectInfo, project_meta: sly.ProjectMeta):
    api = sly.Api()
    global team, workspace, project, meta

    project = project_info
    meta = project_meta
    if len(meta.obj_classes) == 0:
        raise ValueError("App finished: project does not have classes")

    workspace = api.workspace.get_info_by_id(project_info.workspace_id)
    team = api.team.get_info_by_id(workspace.team_id)


def increment(
    dataset: sly.DatasetInfo,
    image: sly.ImageInfo,
    ann: sly.Annotation,
):
    global max_x
    counters = defaultdict(int)
    for label in ann.labels:
        counters[label.obj_class.name] += 1
    for obj_class in meta.obj_classes:
        class_name = obj_class.name
        objects_count = counters[class_name]
        stats[class_name][objects_count]["images_count"] += 1
        max_x = max(max_x, objects_count)
        labeling_url = sly.image.get_labeling_tool_url(
            team.id, workspace.id, project.id, dataset.id, image.id
        )

        stats[class_name][objects_count]["table_rows"].append(
            [
                image.id,
                sly.image.get_labeling_tool_link(labeling_url, image.name),
                dataset.name,
                len(ann.labels),
                image.width,
                image.height,
                sly.app.widgets.Table.create_button("preview"),
            ]
        )


def dict_to_xy(d: dict):
    x = list(range(max_x + 1))
    y = [0] * len(x)
    for px, py in d.items():
        y[px] = py["images_count"]
    return x, y


def get_series():
    for class_name, d in stats.items():
        x, y = dict_to_xy(d)
        yield class_name, x, y


def get_table_data(cls_name, obj_count):
    rows = stats[cls_name][obj_count]["table_rows"]
    df = pd.DataFrame(rows, columns=table_columns)
    return df
