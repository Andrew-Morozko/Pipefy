import itertools

from pipefy.Pipefy import PositionalArg


accumulate = PositionalArg(itertools.accumulate)
chain = PositionalArg(itertools.chain)
chain_from_iterable = PositionalArg(itertools.chain.from_iterable)
combinations = PositionalArg(itertools.combinations)
combinations_with_replacement = PositionalArg(
    itertools.combinations_with_replacement
)
cycle = PositionalArg(itertools.cycle)
dropwhile = PositionalArg(itertools.dropwhile, 1)
filterfalse = PositionalArg(itertools.filterfalse, 1)
groupby = PositionalArg(itertools.groupby, 1)
islice = PositionalArg(itertools.islice)
permutations = PositionalArg(itertools.permutations)
product = PositionalArg(itertools.product)
starmap = PositionalArg(itertools.starmap, 1)
takewhile = PositionalArg(itertools.takewhile, 1)
tee = PositionalArg(itertools.tee)
