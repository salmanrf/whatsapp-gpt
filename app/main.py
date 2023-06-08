
from typing import Annotated
from fastapi import Depends, FastAPI
from app.routes.admin_routes import adminRouter


app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/")
async def getHealthCheck(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

app.include_router(adminRouter, prefix="/api/admins", tags=["admins"])
