from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/flight_booking"
    secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080
    otp_expire_minutes: int = 5

    class Config:
        env_file = ".env"


settings = Settings()