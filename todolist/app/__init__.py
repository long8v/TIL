import os

from flask import Flask
from flask_cors import CORS
from flask_mongoengine import flask_mongoengine
from flask_redis import FlaskRedis

app = Flask(__name__)
CORS(app)

env = os.environ.get('APPLICATION_ENV', 'Development')

app.config.from_object(f'config.{env}')
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)

db = MongoEngine(app)
redis_client = FlaskRedis(app)

my_signals = Namespace()

print(redis_client)