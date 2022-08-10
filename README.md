# interactive-objects-distribution

```python
# for dataset in api.dataset.get_list(project.id):
#     images = api.image.get_list(dataset.id)
#     for batch in sly.batched(images):
#         image_ids = [image.id for image in batch]
#         annotations = api.annotation.download_json_batch(dataset.id, image_ids)
#         for ann_json in annotations:
```