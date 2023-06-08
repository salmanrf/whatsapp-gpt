from app.models.users import UserModel
from app.database.mongo import db


async def getUser(criteria: dict) -> UserModel | None:
    print("criteria", criteria)

    user = await db["users"].find_one(criteria)

    if not user:
        return None

    return UserModel(
        id=user["id"],
        name=user["name"],
        phone_number=user["phone_number"],
        whatsapp_id=""
    )


async def createUser(userDto: UserModel) -> UserModel:
    userData = userDto.dict()

    created = await db["users"].insert_one(userData)
    newUser = await db["users"].find_one({"_id": created.inserted_id})

    return newUser


async def findAllUser(criteria: dict = {}, pagination: dict = {}) -> list[UserModel]:
    users = []

    cursor = db["users"].find(criteria)

    for userDoc in await cursor.to_list(length=None):
        users.append(UserModel(**userDoc))

    return users
