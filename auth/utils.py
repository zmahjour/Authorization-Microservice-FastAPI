import jwt
import datetime
import uuid
import pytz
from core.config import settings


class JWTToken:
    @property
    def jti(self):
        return str(uuid.uuid4())

    def generate_access_token(self, jti, user):
        access_token_payload = {
            "user_username": user.username,
            "exp": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            + settings.ACCESS_EXPIRE_TIME,
            "iat": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")),
            "jti": jti,
        }

        access_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return access_token

    def generate_refresh_token(self, jti, user):
        refresh_token_payload = {
            "user_username": user.username,
            "exp": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            + settings.REFRESH_EXPIRE_TIME,
            "iat": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")),
            "jti": jti,
        }

        refresh_token = jwt.encode(
            refresh_token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return refresh_token

    def generate_access_and_refresh_token(self, user):
        jti = self.jti
        access_token = self.generate_access_token(jti=jti, user=user)
        refresh_token = self.generate_refresh_token(jti=jti, user=user)
        return jti, access_token, refresh_token
