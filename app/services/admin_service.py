from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi import HTTPException
from app.config import settings
from app.database.mongo import db
from app.models.admins import AdminModel
from app.schemas.admin_login_schema import AdminLoginSchema


async def getCurrentAdmin(admin_id: str):
    admin = await getAdmin({"_id": admin_id})

    return admin


async def adminLogin(loginSchema: AdminLoginSchema):
    print("loginDto", loginSchema)

    adminDict = await getAdmin({"username": loginSchema.username})

    print("Found Admin", adminDict)

    if not adminDict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username/password."
        )

    admin: AdminModel | None = AdminModel.fromDict(adminDict)

    hashed = loginSchema.password.encode("utf-8")
    storedHash = admin.password.encode("utf-8")
    passwordMatch = bcrypt.checkpw(hashed, storedHash)

    if not passwordMatch:
        raise HTTPException(
            status_code=400,
            detail={
                "data": None,
                "message": "Incorrect username/password."
            }
        )

    currentDate = datetime.now()
    tokenExpiresIn = currentDate + timedelta(days=1)

    jwtPayload = {
        "sub": str(admin.id),
        "username": admin.username,
        "full_name": admin.full_name,
        "exp": tokenExpiresIn
    }

    accessToken = jwt.encode(
        jwtPayload,
        settings.ADMIN_JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return {
        "access_token": accessToken,
    }


async def adminLogout():
    pass


async def getAdmin(criteria: dict):
    admin = await db["admins"].find_one(criteria)

    return admin
