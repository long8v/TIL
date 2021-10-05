import os
from blinker import Namespace
from datetime import datetime
from redis.sentinel import Sentinel
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
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

# db = MongoEngine(app)

if app.config['USE_SENTINEL']:
    sentinel_ports = app.config['REDIS_SENTINEL_PORT']
    redis_host = app.config['REDIS_HOST']
    sentinel = Sentinel([(redis_host, port)
                        for port in sentinel_ports], 
                        socket_timeout=app.config["REDIS_SOCKET_TIMEOUT"])
    redis_client = sentinel.master_for('mymaster')
else:
    redis_client = FlaskRedis(app)

my_signals = Namespace()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) 
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'cTask {self.id}>'
