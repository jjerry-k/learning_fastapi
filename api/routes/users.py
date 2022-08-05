import secrets
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..schemas import User, UserResponse, db
from ..send_email import send_registration_mail
from ..utils import get_password_hash

router = APIRouter(
    tags=["User Routes"]
)

@router.get("/")
def get():
    return {"msg": "Hello World"}

@router.post("/registration", response_description="Register a user", response_model=UserResponse)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    # Check for duplication
    username_found = await db["users"].find_one({"name": user_info["name"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})

    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username is already taken")
    
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email is already taken")

    # Hashing password
    user_info["password"] = get_password_hash(user_info["password"])

    # Create apikey
    user_info["apiKey"] = secrets.token_hex(30)

    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    # Send email
    await send_registraion_mail("Registrain Successful", 
                                user_info["email"], 
                                {"title": "Registration Succeful", 
                                "name": user_info["name"]})

    return created_user
