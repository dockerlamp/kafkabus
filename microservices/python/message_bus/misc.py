'''
Created on Jan 9, 2018

@author: pawel
'''

import time
import functools


def retry(msg, max_retry, interval_ms):
    def retry_inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for retry_no in range(1, max_retry + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    last_error = err
                    time.sleep(interval_ms/1000)
                    print(msg, 'failed because of', err, 'error, attempt',
                                    '%d of %d' % (retry_no, max_retry))
            if last_error: raise last_error
        return wrapper
    return retry_inner
