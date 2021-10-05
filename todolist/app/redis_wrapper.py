from datetime import timedelta
from redis.sentinel import Sentinel
from . import *

def hset(key, field, value):
    redis_client.hset(key, field, value)
    redis_client.expire(key, app.config["REDIS_EXPIRE_TIME"])
    # redis_client.expire(key, timedelta(seconds=app.config["REDIS_EXPIRE_TIME"]))
    
def hget(key, field, default=0):
    value = redis_client.hget(key, field)
    if value:
        return value
    return default