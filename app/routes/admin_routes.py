
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.admin_login_schema import AdminJwtPayload
import app.services.admin_service as admin_service
from app.utils.authorization import authorizeAdmin

adminRouter = APIRouter(tags=["admins"])


@adminRouter.get("/self")
async def handleGetCurrentAdmin(payload: Annotated[AdminJwtPayload, Depends(authorizeAdmin)]):
    return {
        "status": "success",
        "data": payload
    }


@adminRouter.post("/auth/login")
async def handleAdminLogin(loginSchema: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = await admin_service.adminLogin(loginSchema)

    if result["access_token"]:
        return {
            "token_type": "bearer",
            "access_token": result["access_token"],
        }
