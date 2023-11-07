from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx
import json
from schemas.users import UserRegister


router = APIRouter(prefix="/users", tags=["users"])
