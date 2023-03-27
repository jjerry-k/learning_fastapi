from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from schemas import *

app = FastAPI()

app.users = {}
app.id_count = 1
app.tweets = []

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/sign-up", response_description="Sign up a user")
async def sign_up(user_info: User):
    new_user = user_info.dict()
    new_user["id"] = app.id_count
    app.id_count += 1
    app.users[new_user["id"]] = new_user
    return jsonable_encoder(new_user)

@app.post("/login", response_description="Login a user")
async def login():
    pass

@app.post("/tweet", response_description="Tweet a content")
async def tweet(tweet: Tweet):
    user_id = int(tweet.id)
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(tweet.tweet) > 300:
        return "300자를 초과했습니다", 400

    app.tweets.append({
        "user_id": user_id,
        "tweet": tweet.tweet
    })
    
    return "", 200

@app.post("/follow", response_description="Follow a user")
async def follow(follow: Follow):
    user_id = int(follow.id)
    user_id_to_follow = int(follow.follow)
    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonable_encoder(user)

@app.post("/unfollow", response_description="Unfollow a user")
async def unfollow(unfollow: Unfollow):
    user_id = int(Unfollow.id)
    user_id_to_unfollow = int(Unfollow.follow)
    if user_id not in app.users or user_id_to_unfollow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_unfollow)

    return jsonable_encoder(user)

@app.post("/timeline", response_description="Get a user's timeline ")
async def timeline():
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