from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.User import UserRegister, LoginRequest, User, UserInDB
from ..models.Token import TokenData, Token
from ..config.Config import collection_name
from ..schema.schemas import list_serial
from ..utils.security import hash_password, get_current_user,create_access_token, authenticate_user
from bson import ObjectId

router = APIRouter()


ACESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/")
async def get_users():
    """
    GET all registered users

    Returns:
        - A list of all users in the database
    """
    users = list_serial(collection_name.find())
    return users


@router.post("/Register", status_code=status.HTTP_201_CREATED)
async def Register_user(user: UserRegister):
    """
    POST - Register a user into the database
    - checks if the email is already registered
    - hashes the password before saving
    
    Args
     - user(UserRegister): The user's registration data
    
    Returns
    - A success message indicating the registration of the user
    """
    registered_user = collection_name.find_one({"email": user.email})
    if registered_user:
        raise HTTPException(status_code=400, detail="Email already registered, please Log in")
    user_dict = user.dict()

    user_dict.pop("confirm_password", None)
    user_dict["hashed_password"] = hash_password(user.password)

    del user_dict["password"]

    collection_name.insert_one(user_dict)
    return (f"successfully added the user {user.username}")


@router.post("/login")
async def login_user(data: LoginRequest) -> Token:
    """
    POST - Logs in the user
    - authenticates the user credentials
    - create an access token for the user in session

    Args
     - LoginRequest - User's login data

    Returns
     - Token - Access Token
    """
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": user.username,
            "email": user.email,
            "user_id": str(user.id)
        },
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def get_user(current_user: UserInDB = Depends(get_current_user)):
    """
    GET current logged in user

    Returns:
        - current user in the database
    """
    
    return User(
        username=current_user.username,
        email=current_user.email,
        user_id=current_user.id
    )