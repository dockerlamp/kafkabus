'''
Created on Jan 26, 2018

@author: pawel
'''

import inspect
import importlib
import pkgutil


def register(package):
    registry = {}
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(package.__name__ + '.' + module_name)
        for name, handler in inspect.getmembers(module, inspect.isfunction):
            registry[name] = handler

    return registry
