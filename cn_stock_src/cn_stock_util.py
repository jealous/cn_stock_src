import logging.config
import os
from concurrent.futures import ThreadPoolExecutor

__author__ = 'Cedric Zhuang'


def get_thread_count():
    from multiprocessing import cpu_count
    return cpu_count() + 2


def multi_thread(func, items, call_back=None, thread_count=None):
    if thread_count is None:
        thread_count = get_thread_count()

    results = []
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for result in executor.map(func, items):
            if call_back is not None:
                call_back(result)
            results.append(result)
    return results


def get_file_dir(f):
    return os.path.dirname(os.path.realpath(f))


def read_file_in_same_dir(source_file, filename):
    folder = get_file_dir(source_file)
    the_file = os.path.join(folder, filename)
    with open(the_file, 'r') as f:
        ret = f.read()
    return ret


def config_logger():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            }
        }
    })
