from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Princedein@localhost:5432/ops_manager"

settings = Settings()
