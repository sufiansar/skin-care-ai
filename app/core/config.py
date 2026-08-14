from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "skincare_db"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: Optional[str] = ""
    CLAUDE_API_KEY: Optional[str] = ""
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    OPENROUTER_API_KEY: Optional[str] = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct:free"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 1024
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-2"
    AWS_S3_BUCKET_NAME: str = "transeas"
    AWS_S3_USE_PRESIGNED_URL: bool = True
    AWS_S3_PRESIGNED_URL_EXPIRES_IN: int = 3600
    AWS_S3_PUBLIC_ACCESS: bool = False

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres123"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "skincare_db"
    DATABASE_URL: Optional[str] = None

    @property
    def effective_claude_api_key(self) -> str:
        return (self.CLAUDE_API_KEY or self.ANTHROPIC_API_KEY or "").strip()

    @property
    def effective_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


settings = Settings()