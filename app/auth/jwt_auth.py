from fastapi import HTTPException, status
import jwt
from core.config import settings


class JWTAuthentication:
    async def authenticate(self, request, auth_header):
        try:
            token = self.get_token_from_header(header=auth_header)
        except:
            return None

        try:
            payload = self.decode_jwt_token(token=token)
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature."
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired."
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        jti = payload.get("jti")
        redis = request.app.state.redis

        if not await redis.get(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
            )

        return payload


    @staticmethod
    def get_token_from_header(header):
        token = header.replace("Bearer", "").replace(" ", "")
        return token

    @staticmethod
    def decode_jwt_token(token):
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
