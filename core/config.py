from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Zzy_Personal_Agent"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key"
    
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL: str = "glm-4"
    
    DATABASE_URL: str = "sqlite:///./data/zzy_agent.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    YOUTUBE_API_KEY: Optional[str] = None
    SERVERCHAN_KEY: Optional[str] = None
    PUSHPLUS_TOKEN: Optional[str] = None
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
