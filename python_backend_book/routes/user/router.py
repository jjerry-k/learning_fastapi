from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.user import crud, schema
from routes.user.crud import pwd_context
from models import User

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create(_user_create: schema.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_existing(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    crud.create(db=db, user_create=_user_create)

@router.post("/login", response_model=schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = crud.get(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email
    }

def get_current_user(token: str = Depends(oauth2_scheme),
                        db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = crud.get(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update(_user_update: schema.UserUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_user = crud.get(db, _user_update.username)
    if current_user.id != db_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다.")
    if not pwd_context.verify(_user_update.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="기존 비밀번호가 다릅니다.")
    
    crud.update(db=db, db_user=db_user, user_update=_user_update)