from datetime import timedelta
from redis.sentinel import Sentinel
from . import *

def hset(key, field, value):
    redis_client.hset(key, field, value)
    redis_client.expire(key, timedelta(seconds=app.config["REDIS_EXPIRE_TIME"]))
    
def hget(key, field, default=0):
    try:
        return redis_client.hget(key, field)
    except:
        hset(key, field, default)