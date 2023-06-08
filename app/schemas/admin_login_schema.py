
from pydantic import BaseModel, Field


class AdminJwtPayload(BaseModel):
    sub: str = ""
    username: str = ""
    full_name: str = ""
    exp: str = ""

    def fromDict(payload: dict = {}):
        return AdminJwtPayload.parse_obj(payload)


class AdminLoginSchema(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=6, max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "username": "salmannrf",
                "password": "************"
            }
        }
