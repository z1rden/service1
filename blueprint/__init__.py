import os
import redis
from sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
cache = redis.Redis(host = os.getenv('REDIS_HOST', 'localhost'), port = 6379)