from collections import defaultdict
import functools
from inspect import getargspec, isclass
from copy import deepcopy
from itertools import takewhile
from operator import eq, lt, gt, le, ge


__all__ = ('MObject', 'mob')


class _MObjectMeta(type):
    def __new__(mcs, name, bases, dct):
        dct['_mobject_attributes'] = dict(sum([b.__dict__.get('_mobject_attributes', {}).items() for b in bases], []))
        is_mobject_base_class = all(b == object for b in bases)
        if not is_mobject_base_class:
            for k, v in dct.items():
                if k not in ('__module__', '_mobject_attributes'):
                    dct['_mobject_attributes'][k] = v
                    del dct[k]

        return super(_MObjectMeta, mcs).__new__(mcs, name, bases, dct)


def _count_underscore_prefix(s):
    return len(list(takewhile(lambda c: c == '_', s)))


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
            c = wrap(c)

        c._mobject_arg_names = arg_names
        return c

    def _set_simple_attributes(self, kw):
        nested = defaultdict(dict)
        for k, v in kw.items():
            prefix_count = _count_underscore_prefix(k)
            keys = k[prefix_count:].split('__', 1)
            first_key = k[:prefix_count] + keys[0]
            if len(keys) == 1:
                if isclass(v):
                    v = v()
                if callable(v):
                    v = self._handle_callable(v)
                self.__dict__[first_key] = v
            else:
                nested[first_key][keys[1]] = v

        return nested

    def _set_nested_attributes(self, nested):
        for k, v in nested.items():
            if k in self.__dict__:
                if isinstance(self.__dict__[k], MObject):
                    self.__dict__[k]._set_attributes(v)
                else:
                    raise ValueError("Invalid nesting structure, '{}' is already defined as a simple value".format(k))

            self.__dict__[k] = MObject(**v)

    def __init__(self, **kwargs):
        # Take a copy here to avoid destroying the original values if mutating any of the fields
        base_items = [(k, deepcopy(v)) for k, v in self.__class__.__dict__['_mobject_attributes'].items()]
        self._set_attributes(dict(base_items + kwargs.items()))

    def _set_attributes(self, kv):
        nested = self._set_simple_attributes(kv)
        self._set_nested_attributes(nested)

    def _strings_for(self):
        result = []
        for k, v in self.__dict__.items():
            if '__qualname' in k:
                # Python 3 tweak: special attribute that we do not wish to include
                pass
            elif isinstance(v, MObject):
                result.extend("{0}__{1}".format(k, s) for s in v._strings_for())
            elif callable(v):
                result.append("{0}({1})".format(k, ', '.join(v._mobject_arg_names)))
            else:
                result.append("{0}={1}".format(k, v))

        return result

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, ', '.join(sorted(self._strings_for())))

    def _cmp(self, other, cmp_fn):
        # No comparison of callables done
        self_properties = set(k for k, v in self.__dict__.items() if not callable(v))
        other_properties = set(k for k, v in other.__dict__.items() if not callable(v))

        if not cmp_fn(self_properties, other_properties):
            return False

        return all(getattr(self, p) == getattr(other, p) for p in (self_properties & other_properties))

    def __eq__(self, other):
        return self._cmp(other, cmp_fn=eq)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._cmp(other, cmp_fn=lt)

    def __le__(self, other):
        return self._cmp(other, cmp_fn=le)

    def __gt__(self, other):
        return self._cmp(other, cmp_fn=gt)

    def __ge__(self, other):
        return self._cmp(other, cmp_fn=ge)


mob = MObject
