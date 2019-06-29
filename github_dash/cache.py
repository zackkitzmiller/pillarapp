import logging
import os

from exceptions import RedisEnvironmentNotConfigured

logger = logging.getLogger(__name__)
logging.basicConfig()


try:
    import redis

    REDIS_HOST = os.environ.get('REDIS_HOST', None)
    if REDIS_HOST is None:
        raise RedisEnvironmentNotConfigured

    client = redis.Redis(host=os.environ.get('REDIS_HOST'))
except ImportError:
    logger.warn("redis will not be used")
    pass

