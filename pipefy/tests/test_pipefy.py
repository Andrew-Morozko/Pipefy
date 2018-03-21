import pytest

import pipefy


def multiplier_gen(mult=-1):
    t = yield
    while True:
        t = yield t * mult


def adder_func(iterable, add=2):
    result = []
    for el in iterable:
        result.append(el + add)

    return result


def test_pipefy_func():
    """Test that pipefy successfully chooses right Pipefier"""
    gen_func = pipefy.pipefy(multiplier_gen)
    assert isinstance(gen_func(), pipefy.Pipefy.GeneratorIterator)
    gen = pipefy.pipefy(multiplier_gen())
    assert isinstance(gen, pipefy.Pipefy.GeneratorIterator)
    pos_func = pipefy.pipefy(adder_func)
    assert isinstance(pos_func, pipefy.Pipefy.PositionalArg)
    pos_func_explicit = pipefy.pipefy(adder_func, 0)
    assert isinstance(pos_func_explicit, pipefy.Pipefy.PositionalArg)
    keyword_func = pipefy.pipefy(adder_func, 'iterable')
    assert isinstance(keyword_func, pipefy.Pipefy.KeywordArg)


def test_pipefy_decorator():
    @pipefy.pipefy(arg=1)
    def prepend(item, iterable):
        lst = [item]
        lst.extend(iterable)
        return lst

    pipeline = (
        [1, 2, 3] |
        prepend(0)
    )

    assert list(pipeline) == [0, 1, 2, 3]


def test_basic_genrator():
    """Test that pipefy successfully works for generator"""
    multiplier = pipefy.Pipefy.GeneratorFunction(multiplier_gen)

    pipeline = (
        [-1, 0, 1] |
        multiplier(mult=-1) |  # [1, 0, -1]
        multiplier(2)          # [2, 0, -2]
    )

    result = list(pipeline)
    assert result == [2, 0, -2]


def test_wrong_parameters():
    with pytest.raises(TypeError):
        pipefy.Pipefy.PositionalArg(adder_func, '123')
    with pytest.raises(TypeError):
        pipefy.Pipefy.KeywordArg(adder_func, 123)

    with pytest.raises(TypeError):
        pipefy.pipefy(object())
    with pytest.raises(TypeError):
        pipefy.pipefy(adder_func, object())


def test_basic_functionality():
    """Test that pipefy successfully works for function"""
    adder = pipefy.Pipefy.KeywordArg(adder_func, 'iterable')

    pipeline = (
        [-1, 0, 1] |
        adder(add=2) |  # [1, 2, 3]
        adder(add=3)    # [4, 5, 6]
    )

    result = list(pipeline)
    assert result == [4, 5, 6]
