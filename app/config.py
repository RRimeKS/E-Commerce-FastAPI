from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str = "mysql+pymysql://root:@localhost:3306/test"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost"
    COOKIE_SECURE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()