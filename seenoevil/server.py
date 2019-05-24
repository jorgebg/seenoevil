import asyncio
from datetime import datetime
import multiprocessing
import time

from sanic import Sanic, response
from sanic.exceptions import abort, SanicException
from sanic.log import logger
from sanic_jinja2 import SanicJinja2

from .model import Secret
from . import settings

app = Sanic('seenoevil')
app.static('/static', settings.STATIC_PATH)
jinja = SanicJinja2(app)
last_cleanup = multiprocessing.Value('f', time.time())


@app.route("/", methods=['GET', 'POST'])
async def create(request):
    if request.method == 'POST':
        request.json or abort(400)
        try:
            secret = Secret.deserialize(request.json)
        except (TypeError, ValueError):
            abort(400)
        secret.save(force_insert=True)
        return response.json({
            'path': app.url_for('show', token=secret.token)
        })
    else:
        context = {key.lower(): getattr(settings, key) for key in (
            'MAX_DATA_LENGTH', 'MAX_EXPIRATION', 'MAX_READS'
        )}
        return jinja.render('create.html', request, **context)


@app.route('/secret/<token>')
async def show(request, token):
    Secret.update(reads=Secret.reads - 1).where(
        Secret.token == token,
        Secret.expiration >= datetime.now(),
    ).execute() or abort(404, 'Secret not found')
    secret = Secret.get(Secret.token == token)
    secret.reads > 0 or secret.delete_instance()
    context = secret.serialize()
    if request.headers.get('Accept') == 'application/json':
        return response.json(context)
    return jinja.render('show.html', request, **context)


@app.exception(SanicException)
async def error(request, err):
    context = {
        'error': err.args[0] if err.args else 'Unexpected Error.'
    }
    if request.headers.get('Accept') == 'application/json':
        return response.json(context, status=err.status_code)
    return jinja.render('base.html', request, status=err.status_code, **context)


@app.add_task
async def cleanup():
    """Remove expired secrets every 10 minutes"""
    wait = 60 * 10
    while True:
        if (last_cleanup.value + wait) < time.time():
            with last_cleanup.get_lock():
                deleted = Secret.delete().where(Secret.expiration < datetime.now()).execute()
                last_cleanup.value += time.time()
            logger.info('Cleanup: {} expired secrets deleted.'.format(deleted))
        await asyncio.sleep(wait)
