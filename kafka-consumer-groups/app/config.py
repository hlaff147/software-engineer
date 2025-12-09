"""Configuration settings for the Kafka demo application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "demo-topic"
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
