from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS += (
    "redis_cache",
)

from bundle_config import config

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (config['redis']['host'], config['redis']['port']),
        'OPTIONS': {
            'PASSWORD': config['redis']['password'],
        },
    },
}
