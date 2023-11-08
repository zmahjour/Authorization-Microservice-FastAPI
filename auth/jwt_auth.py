from fastapi import HTTPException, status
import jwt
from core.config import settings


class JWTAuthentication:
    @staticmethod
    def get_token_from_header(header):
        token = header.replace("Bearer", "").replace(" ", "")
        return token

    @staticmethod
    def decode_jwt_token(token):
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        return payload
