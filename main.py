from fastapi import FastAPI
import uvicorn
from api.api_v1.api import router as auth_router


app = FastAPI()


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)