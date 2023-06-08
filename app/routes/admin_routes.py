
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.common import PyObjectId
from app.schemas.admin_login_schema import AdminJwtPayload
import app.services.admin_service as admin_service
import app.services.user_service as user_service
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

    raise HTTPException(500, "Internal error")


@adminRouter.get("/users/{user_id}")
async def handleAdminGetUser(_: Annotated[any, Depends(authorizeAdmin)], user_id: str):
    user = await user_service.getUser({"_id": PyObjectId(user_id)})

    if not user:
        raise HTTPException(404, "User not found")

    return {
        "status": "success",
        "data": user
    }


@adminRouter.get("/users/")
async def handleAdminFindAllUser(_: Annotated[any, Depends(authorizeAdmin)]):
    users = await user_service.findAllUser()

    return {
        "status": "success",
        "data": users
    }
