from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
