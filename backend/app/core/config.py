from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VerityAI"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "verityai"
    POSTGRES_PASSWORD: str = "verityai_password"
    POSTGRES_DB: str = "verityai"
    POSTGRES_PORT: str = "5432"
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY: str = "a-very-secret-key-for-verityai-dev-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
