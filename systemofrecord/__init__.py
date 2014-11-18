import os
import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)

def configure_logging(obj):
    logger = logging.getLogger(obj.__class__.__name__)
    logger.addHandler(logging.StreamHandler())

    if app.config['DEBUG']:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger

# Sentry exception reporting
if 'SENTRY_DSN' in os.environ:
    sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.debug("\nConfiguration\n%s\n" % app.config)


def configure_health():
    from systemofrecord.health import Health
    from systemofrecord.repository import blockchain_object_repository
    from systemofrecord.services import ingest_queue, chain_queue

    Health(app,
           checks=[blockchain_object_repository.health,
                   ingest_queue.health,
                   chain_queue.health
           ])


configure_health()

