from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx
import json
from schemas.users import UserRegister


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def user_register(user: UserRegister):
    user_data = jsonable_encoder(user)
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
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=json.loads(response.text).get("detail"),
            )
