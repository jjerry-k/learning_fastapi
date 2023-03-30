from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.tweet import schema, crud
from routes.user.router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/tweet",
    tags=["Tweet"]
)


# @router.get("/list", response_model=schema.TweetList)
# def tweet_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = '', sortby: str = "date"):
#     total, _tweet_list = crud.get_list(db, skip=page*size, limit=size, keyword=keyword, sortby=sortby)
#     return {"total": total, "tweet_list": _tweet_list}


# @router.get("/detail/{tweet_id}", response_model=schema.Tweet)
# def tweet_detail(tweet_id: int, db: Session = Depends(get_db), page: int = 0, size: int = 3, sortby: str = "voter"):
#     tweet = crud.get(db, tweet_id=tweet_id, skip=page*size, limit=size, sortby=sortby)
#     return tweet

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create(_tweet_create: schema.TweetCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    print(current_user.id, current_user.username)
    crud.create(db=db, tweet_create=_tweet_create, user=current_user)
    
# @router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
# def update(_tweet_update: schema.TweetUpdate, 
#                     db: Session = Depends(get_db),
#                     current_user: User = Depends(get_current_user)):
#     db_tweet = crud.get(db, tweet_id=_tweet_update.tweet_id)
#     if not db_tweet:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
#     if current_user.id != db_tweet.user.id:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다.")
#     crud.update(db=db, db_tweet=db_tweet, tweet_update=_tweet_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete(_tweet_delete: schema.TweetDelete, 
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_tweet = crud.get(db, tweet_id=_tweet_delete.tweet_id)
    if not db_tweet:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_tweet.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다.")
    crud.delete(db=db, db_tweet=db_tweet)

# @router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
# def vote(_tweet_vote: schema.TweetVote,
#                   db: Session = Depends(get_db),
#                   current_user: User = Depends(get_current_user)):
#     db_tweet = crud.get(db=db, tweet_id=_tweet_vote.tweet_id)
#     if not db_tweet:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
#     crud.vote(db=db, db_tweet=db_tweet, db_user=current_user)