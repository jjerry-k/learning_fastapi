from fastapi import FastAPI
from .routes import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)