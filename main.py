from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import aioredis
from api.api_v1.api import router as auth_router
from core.config import settings


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    app.state.redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )
    yield
    await app.state.redis.close()


app = FastAPI(lifespan=redis_lifespan)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
