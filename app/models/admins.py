from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.common import PyObjectId


class AdminModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(min_length=6, max_length=20)
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=6, max_length=255)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "60d5e1d636b7b9f9a9b9b8d7",
                "username": "salmannrf",
                "full_name": "Salman Rizqi Fatih",
            }
        }

    def fromDict(adminDict: dict):
        print("adminDict", adminDict)
        adminDict["pasword"] = ""

        return AdminModel.parse_obj(adminDict)
