class Config:
    USE_SENTINEL = False
    REDIS_EXPIRE_TIME = 600
    REDIS_SOCKET_TIMEOUT = 0.1        
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6001
    REDIS_SENTINEL_PORT = [23679, 23680, 23681]
    REDIS_URL = f'redis://:@{REDIS_HOST}:{REDIS_PORT}/0'

class Development(Config):
    DEBUG = True