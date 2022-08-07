from os import access
from venv import create
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import db
from ..oath2 import create_access_token
from .. import utils

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"name": user_credentials.username})
    if user and utils.verify_password(user_credentials.password, user["password"]):
        access_token = create_access_token({"id": user["_id"]})

        return ({"access_token": access_token, "token_type": "bearer"})

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user credentials"
        )