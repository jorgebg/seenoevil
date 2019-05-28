from os import environ, path
from sanic.log import logger


ENV_FILE = ".env"

SECRET_KEY = environ.get("SECRET_KEY")

if not SECRET_KEY:
    from secrets import choice
    import string

    alphabet = string.ascii_letters + string.digits + string.punctuation
    SECRET_KEY = "".join(choice(alphabet) for i in range(64))
    if path.exists(ENV_FILE):
        logger.warn(
            'Unable to persist SECRET_KEY, `.env` file already exists. Are you running `pipenv run`?'
            f' Temporal value: "{SECRET_KEY}".',
        )
    else:
        with open(ENV_FILE, "w") as f:
            f.write(f'SECRET_KEY="{SECRET_KEY}"\n')


DATABASE_URL = environ.get("DATABASE_URL", "sqlite:///secrets.db")
STATIC_PATH = environ.get("STATIC_PATH", path.join(path.dirname(__file__), "static"))

MAX_DATA_LENGTH = int(environ.get("MAX_DATA_LENGTH", 2 ** 20))
MAX_EXPIRATION = int(environ.get("MAX_EXPIRATION", 7 * 24))  # Hours
MAX_READS = int(environ.get("MAX_READS", 7))

SANIC_CONFIG = {
    "debug": environ.get("DEBUG"),
    "host": environ.get("HOST"),
    "port": int(environ.get("PORT", 8000)),
    "workers": int(environ.get("WORKERS", 1)),
}
