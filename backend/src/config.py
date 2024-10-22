from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_CLUSTER: str
    MONGODB_APPNAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    ADMIN_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    ENVIRONMENT: str = "dev"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()



def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

def get_mongo_db_url():
    return(f"mongodb+srv://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@"
           f"{settings.MONGODB_CLUSTER}/?retryWrites=true&w=majority&appName={settings.MONGODB_APPNAME}")
