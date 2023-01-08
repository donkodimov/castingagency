import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    AUTH0_DOMAIN : str = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID : str = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET : str = os.getenv("AUTH0_CLIENT_SECRET")
    ALGORITHMS : str = os.getenv("ALGORITHMS")
    API_AUDIENCE = str = os.getenv("API_AUDIENCE")
    BASE_URL = os.getenv("BASE_URL")

    PRODUCER = str = os.getenv("PRODUCER")
    DIRECTOR = str = os.getenv("DIRECTOR")
    ASSISTANT = str = os.getenv("ASSISTANT")
    POSTGRES_DB_TEST : str = os.getenv("POSTGRES_DB_TEST","tdd")

settings = Settings()