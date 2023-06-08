
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.config import settings
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from app.schemas.admin_login_schema import AdminJwtPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admins/auth/login")


def authorizeAdmin(token: Annotated[str, Depends(oauth2_scheme)]) -> AdminJwtPayload:
    try:
        payload = jwt.decode(
            token, settings.ADMIN_JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        return AdminJwtPayload.fromDict(payload)
    except ExpiredSignatureError:
        raise HTTPException(detail="Token has expired", status_code=401)
    except InvalidTokenError as e:
        raise HTTPException(detail="Invalid token", status_code=401)
