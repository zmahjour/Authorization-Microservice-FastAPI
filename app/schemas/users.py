from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str


class OtpEmail(BaseModel):
    email: EmailStr


class OtpCodeData(BaseModel):
    email: EmailStr
    username: str
    code: int
