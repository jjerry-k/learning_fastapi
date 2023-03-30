from datetime import datetime

from models import User, Tweet
from sqlalchemy.orm import Session
from routes.tweet.schema import TweetCreate, TweetUpdate

def get(db: Session, tweet_id: int):
    tweet = db.query(Tweet).get(tweet_id)
    db.commit()
    return tweet

def create(db: Session, tweet_create: TweetCreate, user: User):
    db_tweet = Tweet(
                    content=tweet_create.content,
                    create_date=datetime.now(), 
                    user=user)
    db.add(db_tweet)
    db.commit()

def delete(db: Session, db_tweet: Tweet):
    db.delete(db_tweet)
    db.commit()