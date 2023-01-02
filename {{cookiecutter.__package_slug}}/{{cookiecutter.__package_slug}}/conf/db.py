from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
