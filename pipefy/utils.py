from itertools import count
from pipefy import Pipefy


@Pipefy.GeneratorFunction
def observe(printer=print, **printer_kwargs):
    """Prints items as they are passed along"""
    item = yield
    while True:
        printer(item, **printer_kwargs)
        item = yield item


@Pipefy.GeneratorFunction
def observe_enumerated(printer=print, start=0, **printer_kwargs):
    item = yield
    counter = count(start=start)
    while True:
        printer(next(counter), item, **printer_kwargs)
        item = yield item
