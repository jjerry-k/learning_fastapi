from fastapi import FastAPI

from schemas import *

app = FastAPI()

app.users = {}
app.id_count = 1

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/sign-up", response_description="Sign up a user")
async def sign_up(user_info: User):
    pass
# API List
# Sign up
# - id, name, email, password, profile
# Login
# - email, password
# Tweet
# - id, content
# Follow
# - id, follow id
# Unfollow
# - id, unfollow id
# Timeline
# - id