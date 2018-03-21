# from .itertools.recepies import take
# from pipefy import pipefy, std, util, itertools
import pytest

from pipefy import std


def test_enumerate():
    data = list(range(-10, 10))

    pipeline = (
        data |
        std.enumerate()
    )

    alt = enumerate(data)

    assert list(pipeline) == list(alt)


def test_filter():
    data = list(range(-10, 10))

    def less_than_0(x):
        return x < 0

    def abs_less_than_5(x):
        return abs(x) < 5

    pipeline = (
        data |
        std.filter(less_than_0) |
        std.filter(abs_less_than_5)
    )

    alt = filter(
        abs_less_than_5,
        filter(
            less_than_0,
            data
        )
    )

    assert list(pipeline) == list(alt)


def test_map():
    data = list(range(-10, 10))

    def plus_5(x):
        return x + 5

    def times_2(x):
        return x * 2

    pipeline = (
        data |
        std.map(plus_5) |
        std.map(times_2)
    )

    alt = map(
        times_2,
        map(
            plus_5,
            data
        )
    )

    assert list(pipeline) == list(alt)


def test_join():
    data = 'Test string'

    pipeline = (
        data |
        std.join('|')
    )

    alt = '|'.join(data)
    assert pipeline == alt


@pytest.mark.parametrize("func_name,data", [
    ('bytearray', [0x41, 0x42, 0x43]),
    ('bytes', [0x41, 0x42, 0x43]),
    ('dict', list(zip(range(10), range(10, 20)))),
    ('frozenset', [1, 2, 3, 1, 2]),
    ('list', 'Test String'),
    ('max', list(range(10))),
    ('min', list(range(10))),
    ('set', [1, 2, 3, 1, 2]),
    ('sorted', [5, 2, 3, 1, 4]),
    ('str', 12345),
    ('sum', list(range(10))),
    ('tuple', list(range(10))),
])
def test_against_std_func(func_name, data):
    piped_func = eval(f'std.{func_name}')
    std_func = eval(f'{func_name}')

    pipeline = (
        data |
        piped_func()
    )

    alt = std_func(data)

    assert pipeline == alt
