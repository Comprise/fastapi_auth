from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_secret: str
    app_token_alg: str = 'HS256'
    app_access_lifetime: int = 30
    app_refresh_token_lifetime: int = 600

    db_url: str
    allow_origins: List

    class Config:
        env_file = 'config/.env'


settings = Settings()
