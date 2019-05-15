from .server import app
from . import settings

app.run(**settings.SANIC_CONFIG)
