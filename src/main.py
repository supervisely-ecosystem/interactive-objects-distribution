import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from supervisely.app.fastapi import create, Jinja2Templates, available_after_shutdown

import supervisely as sly
from supervisely.sly_logger import logger
from supervisely.app import DataJson, StateJson


app_root_directory = str(Path(__file__).parent.absolute().parents[0])
logger.info(f"App root directory: {app_root_directory}")
app_data_dir = os.path.join(app_root_directory, 'tempfiles')
app_cache_dir = os.path.join(app_data_dir, 'cache')

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()
file_cache = sly.FileCache(name="FileCache", storage_root=app_cache_dir)
app = FastAPI()
sly_app = create()

app.mount("/sly", sly_app)
app.mount("/static", StaticFiles(directory=os.path.join(app_root_directory, 'static')), name="static")
templates_env = Jinja2Templates(directory=os.path.join(app_root_directory, 'templates'))


project_id = int(os.environ["modal.state.slyProjectId"])
project_info = api.project.get_info_by_id(project_id)

DataJson()['project_id'] = project_id
DataJson()['project_name'] = project_info.name
DataJson()['project_preview_url'] = api.image.preview_url(project_info.reference_image_url, 100, 100)

@app.get("/")
@available_after_shutdown(app=app)
def read_index(request: Request):
    return templates_env.TemplateResponse('index.html', {'request': request})