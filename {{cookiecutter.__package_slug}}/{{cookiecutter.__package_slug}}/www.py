import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

static_file_path = os.path.dirname(os.path.realpath(__file__)) + "/static"
app.mount("/static", StaticFiles(directory=static_file_path), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}
