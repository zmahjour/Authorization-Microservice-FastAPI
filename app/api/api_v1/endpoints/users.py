from fastapi import APIRouter, status, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx
import json
from schemas.users import UserRegister, UserLogin, OtpEmail, OtpCodeData
from auth.utils import JWTToken
from auth.jwt_auth import auth
from core.config import settings


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def user_register(user: UserRegister):
    user_data = jsonable_encoder(user)
    del user_data["confirm_password"]
    account_register_url = f"{settings.ACCOUNT_APP_BASE_URL}/account/register"

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
    account_login_url = f"{settings.ACCOUNT_APP_BASE_URL}/account/login"
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
            username=user.username
        )
        refresh_exp_seconds = settings.REFRESH_EXPIRE_TIME.total_seconds()

        await redis.set(jti, "whitelist", int(refresh_exp_seconds))

        return JSONResponse(
            content={"access_token": access_token, "refresh_token": refresh_token},
            status_code=response.status_code,
        )


@router.post("/otp/login")
async def otp_login(otp_email: OtpEmail):
    data = jsonable_encoder(otp_email)
    account_otp_login_url = f"{settings.ACCOUNT_APP_BASE_URL}/account/otp/login"
    notification_send_email_url = f"{settings.NOTIFICATION_APP_BASE_URL}/notif/email"

    async with httpx.AsyncClient() as client:
        response = await client.post(url=account_otp_login_url, json=data)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=response.status_code,
            detail=json.loads(response.text).get("detail"),
        )
    elif response.status_code == status.HTTP_200_OK:
        async with httpx.AsyncClient() as client:
            notif_response = await client.post(
                url=notification_send_email_url, json={"email": [data["email"]]}
            )

        username = json.loads(response.text).get("username")

        return JSONResponse(
            content=json.loads(notif_response.text),
            status_code=response.status_code,
        )


@router.post("/otp/verify")
async def otp_verify(request: Request, otp: OtpCodeData):
    otp_code = otp.code
    redis = request.app.state.redis
    cached_code = await redis.get(otp.email)

    if cached_code and int(cached_code.decode("utf-8")) == otp_code:
        jwt_token = JWTToken()
        jti, access_token, refresh_token = jwt_token.generate_access_and_refresh_token(
            username=otp.username
        )
        refresh_exp_seconds = settings.REFRESH_EXPIRE_TIME.total_seconds()

        await redis.set(jti, "whitelist", int(refresh_exp_seconds))

        return JSONResponse(
            content={"access_token": access_token, "refresh_token": refresh_token},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"detail": "Invalid code."},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )


@router.get("/logout", status_code=status.HTTP_200_OK)
async def user_logout(request: Request, authorization: str = Header()):
    payload = await auth.authenticate(request=request, auth_header=authorization)

    if payload:
        jti = payload.get("jti")
        await auth.delete_jti_from_cache(request=request, jti=jti)

        return "You have logged out successfully."


@router.post("/token")
async def obtain_access_token():
    pass
