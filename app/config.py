from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str = "mysql+pymysql://root:@localhost:3306/test"
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()