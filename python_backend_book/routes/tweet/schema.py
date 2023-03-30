import datetime
from typing import Union
from pydantic import BaseModel, validator

from routes.user.schema import User

class Tweet(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: Union[User, None]
    
    class Config:
        orm_mode = True

class TweetCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class TweetList(BaseModel):
    total: int = 0
    tweet_list: list[Tweet] = []
    
class TweetUpdate(TweetCreate):
    tweet_id: int

class TweetDelete(BaseModel):
    tweet_id: int