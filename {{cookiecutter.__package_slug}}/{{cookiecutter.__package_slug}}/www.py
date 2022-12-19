import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
{%- if cookiecutter.include_jinja2 == "y" %}
from fastapi.templating import Jinja2Templates
{%- endif %}

static_file_path = os.path.dirname(os.path.realpath(__file__)) + "/static"

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_file_path), name="static")
{%- if cookiecutter.include_jinja2 == "y" %}
templates = Jinja2Templates(directory="templates")
{%- endif %}

@app.get("/")
async def root():
    return {"message": "Hello World"}
