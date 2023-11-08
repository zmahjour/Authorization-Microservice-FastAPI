from fastapi import HTTPException, status
import jwt
from core.config import settings


class JWTAuthentication:
    @staticmethod
    def get_token_from_header(header):
        token = header.replace("Bearer", "").replace(" ", "")
        return token

