from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import router
from app.db import init_db

# 应用生命周期中触发数据库初始化


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Event Service", version="0.1.0", lifespan=lifespan)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
