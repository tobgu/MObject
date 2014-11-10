from collections import defaultdict
import functools
from inspect import getargspec
from copy import copy, deepcopy


class _MObjectMeta(type):
    def __new__(mcs, name, bases, dct):
        dct['_mobject_attributes'] = copy(bases[0].__dict__.get('_mobject_attributes', {}))
        if bases[0] != object:
            for k, v in dct.items():
                if k not in ('__module__', '_mobject_attributes'):
                    dct['_mobject_attributes'][k] = v
                    del dct[k]

        return super(_MObjectMeta, mcs).__new__(mcs, name, bases, dct)


class MObject(object):
    __metaclass__ = _MObjectMeta

    def _handle_callable(self, c):
        def wrap(f):
            @functools.wraps(f)
            def instance_fn_wrapper(*args, **kws):
                return f(self, *args, **kws)
            return instance_fn_wrapper

        arg_names = getargspec(c).args
        if len(arg_names) > 0 and arg_names[0] == 'self':
            return wrap(c)

        return c

    def _assign_simple_values(self, kw):
        nested = defaultdict(dict)
        for k, v in kw.items():
            keys = k.split('__', 1)
            if len(keys) == 1:
                if callable(v):
                    v = self._handle_callable(v)
                self.__dict__[keys[0]] = v
            else:
                nested[keys[0]][keys[1]] = v

        return nested

    def _assign_nested_values(self, nested):
        for k, v in nested.items():
            if k in self.__dict__:
                raise ValueError("Invalid nesting structure, '{}' is already defined as a simple value".format(k))

            self.__dict__[k] = MObject(**v)

    def __init__(self, **kwargs):
        # Deed to take a copy here to avoid destroying the original values if mutatnig any of the fields
        base_items = [(k, deepcopy(v)) for k, v in self.__class__.__dict__['_mobject_attributes'].items()]
        nested = self._assign_simple_values(dict(base_items + kwargs.items()))
        self._assign_nested_values(nested)
