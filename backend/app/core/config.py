import os


class Settings:
    PROJECT_NAME: str = "Property Finder"
    PROJECT_VERSION: str = "1.0.0"

    PRODUCTION_DATABASE_URL: str = os.getenv("PRODUCTION_DATABASE_URL", "sqlite:///./app/production.db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "sqlite:///./app/tests/test.db")

    DATABASE_URL: str = os.getenv("DATABASE_URL", PRODUCTION_DATABASE_URL)


settings = Settings()
