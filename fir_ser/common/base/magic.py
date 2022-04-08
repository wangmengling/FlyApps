#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 12月 
# author: NinEveN
# date: 2021/12/22
import datetime
import logging
import time
from functools import wraps
from importlib import import_module

from django.core.cache import cache

logger = logging.getLogger(__name__)


def run_function_by_locker(timeout=60 * 5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            locker = kwargs.get('locker', {})
            if locker:
                kwargs.pop('locker')
            t_locker = {'timeout': timeout, 'locker_key': func.__name__}
            t_locker.update(locker)
            new_locker_key = t_locker.pop('locker_key')
            new_timeout = t_locker.pop('timeout')
            if locker and new_timeout and new_locker_key:
                with cache.lock(new_locker_key, timeout=new_timeout, **t_locker):
                    logger.info(f"{new_locker_key} exec {func} start. now time:{time.time()}")
                    res = func(*args, **kwargs)
            else:
                res = func(*args, **kwargs)
            logger.info(f"{new_locker_key} exec {func} finished. used time:{time.time() - start_time} result:{res}")
            return res

        return wrapper

    return decorator


def call_function_try_attempts(try_attempts=3, sleep_time=2, failed_callback=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = False, {}
            start_time = time.time()
            for i in range(try_attempts):
                res = func(*args, **kwargs)
                status, result = res
                if status:
                    return res
                else:
                    logger.warning(f'exec {func} failed. {try_attempts} times in total. now {sleep_time} later try '
                                   f'again...{i}')
                time.sleep(sleep_time)
            if not res[0]:
                logger.error(f'exec {func} failed after the maximum number of attempts. Failed:{res[1]}')
                if failed_callback:
                    logger.error(f'exec {func} failed and exec failed callback {failed_callback.__name__}')
                    failed_callback(*args, **kwargs, result=res)
            logger.info(f"exec {func} finished. time:{time.time() - start_time} result:{res}")
            return res

        return wrapper

    return decorator


def magic_wrapper(func, *args, **kwargs):
    @wraps(func)
    def wrapper():
        return func(*args, **kwargs)

    return wrapper


def magic_notify(notify_rules, timeout=30 * 24 * 60 * 60):
    """
    :param notify_rules:
    :param timeout:
    :return:
    """
    now_time = datetime.datetime.now().date()
    for notify_rule in notify_rules:
        notify_cache = notify_rule['cache']
        if notify_rule['func']():
            notify_data = notify_cache.get_storage_cache()
            if notify_data is None:
                notify_cache.set_storage_cache([now_time + datetime.timedelta(days=i) for i in notify_rule['notify']],
                                               timeout)
                magic_notify(notify_rules)
            elif isinstance(notify_data, list):
                if len(notify_data) == 0:
                    return
                else:
                    notify_data.append(now_time)
                    notify_data.sort()
                    is_today = False
                    if notify_data[0] == notify_data[1]:
                        is_today = True
                    notify_data = list(set(notify_data))
                    notify_data.sort()
                    n_index = notify_data.index(now_time)
                    if n_index == 0 and not is_today:
                        return
                    notify_data = notify_data[n_index + 1:]

                    for func in notify_rule['notify_func']:
                        try:
                            func()
                        except Exception as e:
                            logger.error(f'func {func.__name__} exec failed Exception:{e}')
                    notify_cache.set_storage_cache(notify_data, timeout)

        else:
            notify_cache.del_storage_cache()


def import_from_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
                          ) from err
