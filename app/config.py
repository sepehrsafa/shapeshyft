TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        }
    },
}

AUTH = {
    "SECRET_KEY": "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 1000,
    "REFRESH_TOKEN_EXPIRE_DAYS": 30,
}

ENCRYPTION_KEY = b"TMWqqeqUi9Ip8vRz7iuc0O16BC6XY-FUOBbOEl-zvog="

PASSWORD_HASH_SECRET = b"your_secret_key_here"

