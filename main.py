from enum import Enum

from typing import Optional, List

from pydantic import BaseModel

from fastapi import FastAPI, Query, Path, Body, Request
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

# Query Parameters
@app.get("/query_params/")
async def read_items(q: Optional[str] = Query("Default Value", title="Query Parameters", min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    print(q)
    if q:
        results.update({"q": q})
        results.update({"title": q.title()})
    return results

@app.get("/query_multi/")
async def read_items(q: Optional[List[str]] = Query(None, title="Query Multiple Parameters")):
    query_items = {"q": q}
    return query_items

# Path Parameters
@app.get("/path_params/{item_id}")
async def read_items(q: str, item_id: int = Path(..., title="The ID of the item to get", ge=1)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Declare Request Example Data

class ExampleItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/multiple_example/{item_id}")
async def read_items(
    *,
    item_id: int,
    item: ExampleItem = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
templates = Jinja2Templates(directory="templates")

@app.get("/jinja/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
