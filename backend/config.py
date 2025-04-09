from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TalentMatch AI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./talentmatch.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # SMTP Configuration
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    class Config:
        env_file = ".env"

settings = Settings()