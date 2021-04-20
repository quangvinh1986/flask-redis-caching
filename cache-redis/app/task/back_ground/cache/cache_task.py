import json
from datetime import datetime
from celery.utils.log import get_task_logger
import redis


logger = get_task_logger(__name__)


class CommonCacheTask:

    def __init__(self, config):
        self.config = config
        self.redis_controller = self.init_redis(config)

    def get_from_cache(self, key):
        try:
            value = self.redis_controller.get(key)
            return value
        except Exception as ex:
            return None

    def save_to_cache(self, key, data):
        value = {
            'data': data,
            'dateReceived': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'isCache': True
        }
        try:
            self.redis_controller.set(key, json.dumps(value))
            return value
        except Exception as ex:
            value['isCache'] = False
            return value

    def init_redis(self, config):
        if self.config.get('REDIS_PASSWORD'):
            r = redis.Redis(host=self.config.get("REDIS_HOST"),
                            port=self.config.get('REDIS_PORT'),
                            db=self.config.get('REDIS_DB'),
                            password=self.config.get('REDIS_PASSWORD')
                            )
            return r
        else:
            r = redis.Redis(host=self.config.get("REDIS_HOST"),
                            port=self.config.get('REDIS_PORT'),
                            db=self.config.get('REDIS_DB')
                            )
            return r
