from collections import defaultdict
import supervisely as sly


def dict_to_xy(d: dict, max_x: int):
    x = list(range(max_x + 1))
    y = [0] * len(x)
    for px, py in d.items():
        y[px] = py
    return x, y


def increment_stats(
    stats,
    tables_rows,
    max_x,
    dataset: sly.DatasetInfo,
    image: sly.ImageInfo,
    ann: sly.Annotation,
    meta: sly.ProjectMeta,
):
    counters = defaultdict(int)
    for label in ann.labels:
        counters[label.obj_class.name] += 1
    for obj_class in meta.obj_classes:
        class_name = obj_class.name
        objects_count = counters[class_name]
        stats[class_name][objects_count] += 1
        max_x = max(max_x, objects_count)
        tables_rows[class_name][objects_count].append(
            [
                image.id,
                image.name,
                dataset.name,
                len(ann.labels),
                image.width,
                image.height,
            ]
        )
    return max_x
