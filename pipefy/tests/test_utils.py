import pytest

import pipefy


def simple_gen():
    yield from range(10)


def test_observe():
    result = ''

    def printer(*items):
        nonlocal result
        result += ' '.join(map(str, items)) + '\n'

    pipeline = (
        simple_gen() |
        pipefy.utils.observe(printer=printer)
    )
    _ = list(pipeline)

    assert result == ''.join(
        map(
            lambda item: f'{item}\n',
            simple_gen()
        )
    )


def test_observe_enumerated():
    result = ''

    def printer(*items):
        nonlocal result
        result += ' '.join(map(str, items)) + '\n'

    pipeline = (
        simple_gen() |
        pipefy.utils.observe_enumerated(printer=printer)
    )
    _ = list(pipeline)

    assert result == ''.join(
        map(
            lambda item: f'{item[0]} {item[1]}\n',
            enumerate(simple_gen())
        )
    )
