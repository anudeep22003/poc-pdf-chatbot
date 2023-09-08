from starlette.config import Config
from starlette.datastructures import (
    Secret,
)  # prevents secrets from leaking into tracebacks. to use cast into string

# Config will be read from environment variables and/or ".env" files
config = Config(".env")

OPENAI_API_KEY = config("OPENAI_API_KEY", cast=Secret)

SIMILARITY_TOP_K = 3
