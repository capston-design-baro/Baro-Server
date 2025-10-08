from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str
    OPENAI_API_KEY: str
    BARO_AI_URL: str = "http://localhost:8001"  # Baro-AI 서비스 URL

    class Config:
        env_file = ".env"

settings = Settings()