import os
from dotenv import load_dotenv

load_dotenv()

# Env variables
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PORT = os.getenv("SERVER_PORT")

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

POSTGRESQL_URL = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DATABASE}"
)

ADMIN_TOOLS_ON = os.getenv("ADMIN_TOOLS_ON").lower() == "true"
DISABLE_DATABASE = os.getenv("DISABLE_DATABASE").lower() == "true"

WORKER_HOST = os.getenv("WORKER_HOST")
WORKER_PORT = os.getenv("WORKER_PORT")

WORKER_URL = f"http://{WORKER_HOST}:{WORKER_PORT}/"

ADMIN_TOOLS_KEY = os.getenv("ADMIN_TOOLS_KEY")

ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://0.0.0.0:8000",
    f"http://0.0.0.0:{SERVER_PORT}",
    "http://localhost",
    "http://localhost:8000",
    f"http://localhost:{SERVER_PORT}",
    f"http://{SERVER_ADDRESS}",
]
