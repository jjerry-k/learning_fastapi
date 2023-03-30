import yaml

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routes.user import router as user_router
from routes.tweet import router as tweet_router

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["ORIGIN"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(tweet_router.router)
# app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@app.get("/")
def index():
    return {"msg":"Hello, World"}
    # return FileResponse("frontend/dist/index.html")
