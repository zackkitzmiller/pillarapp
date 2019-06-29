import os

import redis

client = redis.Redis(host=os.environ.get('REDIS_HOST'))
