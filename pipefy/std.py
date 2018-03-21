from pipefy.Pipefy import PositionalArg

bytearray = PositionalArg(bytearray)
bytes = PositionalArg(bytes)
dict = PositionalArg(dict)
enumerate = PositionalArg(enumerate)
filter = PositionalArg(filter, 1)
frozenset = PositionalArg(frozenset)
list = PositionalArg(list)
map = PositionalArg(map, 1)
max = PositionalArg(max)
min = PositionalArg(min)
set = PositionalArg(set)
sorted = PositionalArg(sorted)
str = PositionalArg(str)
sum = PositionalArg(sum)
tuple = PositionalArg(tuple)


@PositionalArg
def join(iterable, by=''):
    return by.join(iterable)
