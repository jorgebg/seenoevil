import os

from environs import Env


env = Env()

if not (env.str("SECRET_KEY", '') or os.path.exists('.env')):
    from secrets import choice
    import string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(choice(alphabet) for i in range(64))
    with open('.env', 'w') as f:
        f.write(f'SECRET_KEY="{secret_key}"\n')


env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
DATABASE_URL = env.str("DATABASE_URL", "sqlite:///secrets.db")

MAX_DATA_LENGTH = env.int("MAX_DATA_LENGTH", 2**13)
MAX_EXPIRATION = env.int("MAX_EXPIRATION", 7 * 24)  # Hours
MAX_READS = env.int("MAX_READS", 7)

SANIC_CONFIG = {
    'debug': env.bool("DEBUG", False),
    'host': env.str("HOST", None),
    'port': env.int("PORT", None),
    'workers': env.int("WORKERS", 1),
}
