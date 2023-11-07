from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx
import json
from schemas.users import UserRegister, UserLogin
from auth.jwt import JWTToken
from core.config import settings


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def user_register(user: UserRegister):
    user_data = jsonable_encoder(user)
    del user_data["confirm_password"]
    account_register_url = "http://localhost:8001/account/register"

    async with httpx.AsyncClient() as client:
        response = await client.post(url=account_register_url, json=user_data)

    if response.status_code == status.HTTP_406_NOT_ACCEPTABLE:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=json.loads(response.text).get("detail"),
        )
    elif response.status_code == status.HTTP_409_CONFLICT:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=json.loads(response.text).get("detail"),
        )
    elif response.status_code == status.HTTP_201_CREATED:
        return JSONResponse(
            content=json.loads(response.text), status_code=status.HTTP_201_CREATED
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=json.loads(response.text).get("detail"),
        )


@router.post("/login")
async def user_login(request: Request, user: UserLogin):
    user_data = jsonable_encoder(user)
    account_login_url = "http://localhost:8001/account/login"
    redis = request.app.state.redis

    async with httpx.AsyncClient() as client:
        response = await client.post(url=account_login_url, json=user_data)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=response.status_code,
            detail=json.loads(response.text).get("detail"),
        )
    elif response.status_code == status.HTTP_400_BAD_REQUEST:
        raise HTTPException(
            status_code=response.status_code,
            detail=json.loads(response.text).get("detail"),
        )
    elif response.status_code == status.HTTP_200_OK:
        jwt_token = JWTToken()
        jti, access_token, refresh_token = jwt_token.generate_access_and_refresh_token(
            user=user
        )
        refresh_exp_seconds = settings.REFRESH_EXPIRE_TIME.total_seconds()

        await redis.set(jti, "whitelist", int(refresh_exp_seconds))

        return JSONResponse(
            content={"access_token": access_token, "refresh_token": refresh_token},
            status_code=response.status_code,
        )


@router.get("/logout")
async def user_logout():
    pass


