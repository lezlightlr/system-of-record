from redis import Redis
import urlparse
from cPickle import dumps, loads

from systemofrecord import app



# This module is a wrapper around Redis for queueing features. If we wish to switch
# queueing provider then we only need to change this wrapper.
class RedisQueueProvider(object):
    def __init__(self, queue_name):
        self.queue_name = queue_name
        redis_url = urlparse.urlparse(app.config.get('REDIS_URL'))

        self.redis_server = Redis(
            host=redis_url.hostname,
            port=redis_url.port,
            password=redis_url.password
        )

    def add_to_queue(self, data):
        self.redis_server.rpush(self.queue_name, dumps(data))

    def read_from_queue(self):
        return loads(self.redis_server.blpop(self.queue_name)[1])

    def queue_size(self):
        return self.redis_server.llen(self.queue_name)

    def is_empty(self):
        return self.queue_size() == 0

    def health(self):
        try:
            self.redis_server.info()
            return True, "Redis"
        except Exception as e:
            self.logger.error("Healthcheck failed [%s]" % e)
            return False, "Redis"