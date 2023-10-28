from fastapi import FastAPI

from . import schemas

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
