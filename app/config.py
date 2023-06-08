
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str
    MONGO_INITDB_DATABASE: str
    WEBHOOK_VERIFY_TOKEN: str
    OPEN_AI_API_KEY: str
    FACEBOOK_API_URL: str
    WHATSAPP_ACCESS_TOKEN: str
    ADMIN_JWT_SECRET: str
    JWT_ALGORITHM: str

    class Config:
        env_file = "./app/.env"


settings = Settings()
