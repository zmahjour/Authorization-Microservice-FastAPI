from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    _id: str
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    _id: str
    username: str | None
    email: EmailStr | None
    password: str
