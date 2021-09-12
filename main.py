from enum import Enum

from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
# def root():
async def root():
    return "Hello, FastAPI!"

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
    
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# 127.0.0.1:8000/length/?skip=0&limit=23
@app.get("/length")
def read_item(skip: int=0, limit: int=10):
    return [i for i in range(skip, limit)]

@app.post("/pydantic")
async def read_item(item: Item):
    return item

@app.get("/query")
def read_item(q: Optional[str] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

templates = Jinja2Templates(directory="templates")

@app.get("/jinja/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
