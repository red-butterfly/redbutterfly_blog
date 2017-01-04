import ConfigParser

import redis
from django.utils import lru_cache

from conf.settings import DEFAULT_CONFIG_FILE, SECTION_REDIS, server_logger

REDIS_HOST = 'host'
REDIS_PORT = 'port'
REDIS_DB = 'db'


class BaseRedis(object):

    def __init__(self, config_file, config_section_name, logger=None):
        self.logger = logger
        self.host = None
        self.port = None
        self.db = None
        self.rh = None
        self.create_redis_handler(config_file, config_section_name)

    def create_redis_handler(self, config_file, config_section_name):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(config_file)
            self.host = cf.get(config_section_name, REDIS_HOST)
            self.port = cf.get(config_section_name, REDIS_PORT)
            self.db = cf.get(config_section_name, REDIS_DB)
            self.rh = redis.Redis(host=self.host, port=self.port, db=self.db)
            if self.logger != None:
                self.logger.debug('BaseRedis create redis ({host},{port},{db})OK!'.format(host=self.host,port=self.port,db=self.db))
        except Exception, e:
            if self.logger != None:
                self.logger.error('BaseRedis create redis Error ,except:{e}'.format(e=e))
            else:
                print e

    def reconnect(self):
        try:
            self.rh = redis.Redis(host=self.host, port=self.port, db=self.db)
            if self.logger != None:
                self.logger.info('BaseRedis reconnect redis OK!')
        except Exception, e:
            if self.logger != None:
                self.logger.error('BaseRedis reconnect redis Error ,except:{e}'.format(e=e))
            else:
                print e

    def set(self, key, value):
        return self.rh.set(key, value)

    def set_expire(self, key, value, timeout):
        return self.rh.setex(key, timeout, value)

    def get(self, key):
        return self.rh.get(key)

    def cache(self, key, value, timeout):
        return self.rh.set(key, value, timeout)

    def expire(self, key, value):
        return self.rh.expire(key, value)

    def delete(self, key):
        return self.rh.delete(key)

    def exists(self, key):
        return self.rh.exists(key)

    def incr(self, key, amount=1):
        return self.rh.incr(key, amount)

    def keys(self, prefix):
        return self.rh.keys(prefix)


@lru_cache.lru_cache(maxsize=None)
def getmyredis(config_file=None, config_section_name=None, logger=None):
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        config_section_name = SECTION_REDIS
        logger = server_logger
    return BaseRedis(config_file, config_section_name, logger)
