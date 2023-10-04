from pydantic_settings import BaseSettings, SettingsConfigDict


class TortoiseSettings(BaseSettings):
    db_connection: str = "postgres://ksffmjucuemboo:c9b62cc1a63bea9f73e67b9d162b305b7e8528752cb3cdb1cda656ccb64007fb@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d2pf8si7oigpvs"


class AuthSettings(BaseSettings):
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1000
    refresh_token_expire_days: int = 30


class PasswordSettings(BaseSettings):
    encryption_key: bytes = b"MWqqeqUi9Ip8vRz7iuc0O16BC6XY-FUOBbOEl-zvog="
    password_hash_secret: bytes = b"your_secret_key_here"


# Create settings instance
tortoise_settings = TortoiseSettings()
auth_settings = AuthSettings()
password_settings = PasswordSettings()
