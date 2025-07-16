from pydantic import BaseModel, EmailStr, Field, model_validator
from ..utils.pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @model_validator(mode='after')
    def check_password_match(self) -> 'UserRegister':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Passwords do not match")
        return self
class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
class LoginRequest(BaseModel):
    email: str
    password: str