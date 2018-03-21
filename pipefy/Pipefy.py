from abc import ABC, abstractmethod
import collections.abc as abc_types
from functools import wraps
from contextlib import suppress
import inspect


class Pipefier(ABC):  # pragma: no cover
    @abstractmethod
    def __ror__(self, data):
        """Will be called when data is piped in"""
        pass


class PositionalArg(Pipefier):
    __slots__ = '_func', '_argument', '_args', '_kwargs'

    def __init__(self, func, argument=0):
        if not isinstance(argument, int):
            raise TypeError('Argument must be int')
        self._argument = argument
        self._func = func

    def __call__(self, *args, **kwargs):
        """Remember call arguments, delay execution untill
        data is piped in from the left"""
        self._args = list(args)
        self._kwargs = kwargs
        return self

    def __ror__(self, data):
        self._args.insert(self._argument, data)
        return self._func(*self._args, **self._kwargs)


class KeywordArg(Pipefier):
    __slots__ = '_func', '_argument', '_args', '_kwargs'

    def __init__(self, func, argument):
        if not isinstance(argument, str):
            raise TypeError('Argument must be str')
        self._argument = argument
        self._func = func

    def __call__(self, *args, **kwargs):
        """Remember call arguments, delay execution untill
        data is piped in from the left"""
        self._args = args
        self._kwargs = kwargs
        return self

    def __ror__(self, data):
        self._kwargs[self._argument] = data
        return self._func(*self._args, **self._kwargs)


class GeneratorIterator(Pipefier):
    __slots__ = ('_gen',)

    def __init__(self, gen, needs_priming=True):
        if needs_priming:
            gen.send(None)
        self._gen = gen

    @staticmethod
    def _forwarder_gen(input_data, gen):
        for piece in input_data:
            yield gen.send(piece)

    def __ror__(self, data):
        return self._forwarder_gen(data, self._gen)


# Faking class name for consistency. Sorry, python gods.
def GeneratorFunction(gen_func):
    """Turns every generator iterator created by gen_func
    into Pipefied generator"""
    @wraps(gen_func)
    def wraper(*args, **kwargs):
        return GeneratorIterator(gen_func(*args, **kwargs))
    return wraper


def pipefy(obj=None, arg=0, *, needs_priming=True):
    """
    Automatically apply appropriate Pipefier.
    """
    if obj is None:
        # called as parametrized decorator
        def decorator(func):
            return pipefy(func, arg=arg, needs_priming=needs_priming)
        return decorator
    elif inspect.isgenerator(obj):
        return GeneratorIterator(obj, needs_priming)
    elif inspect.isgeneratorfunction(obj):
        return GeneratorFunction(obj)
    elif callable(obj):
        if isinstance(arg, int):
            return PositionalArg(obj, arg)
        if isinstance(arg, str):
            return KeywordArg(obj, arg)
        raise TypeError('Pipefied argument must be ether int or str')
    else:
        raise TypeError(f"Don't know how to pipefy this {obj}")

# This is quite useless :-/

# try:
#     import wrapt

#     class PipefyShield(wrapt.ObjectProxy):
#         def __or__(self, other):
#             if isinstance(other, Pipefier):
#                 return other.__ror__(self)
#             else:
#                 return self.__wrapped__ | other

#     def shield(obj):
#         """
#         Wraps object, that supports __or__ (and does something,
#         even when operand is of unknown type). Resulting object
#         is safe for use everywhere, and supports Pipefy
#         """
#         if not callable(getattr(obj, '__or__', None)):
#             # There's need to wrap, let's not waste time
#             return obj
#         else:
#             return PipefyShield(obj)


# except ModuleNotFoundError:
#     pass
