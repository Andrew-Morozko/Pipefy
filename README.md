# Pipefy

_Unix-like pipelines for python generators_

# Example

```py
from pipefy import pipefy, std, itertools, utils
from functools import partial


def gen_fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, b+a


@pipefy
def halver():
    n = 0
    while True:
        n = yield n//2


def main():
    pipeline = (
        gen_fib() |  # 1, 1, 2, 3, 5, 8...
        utils.observe(printer=partial(print, "Number:  ")) |
        std.filter(lambda x: x % 2 == 0) |  # 2, 8, 34, 144...
        utils.observe(printer=partial(print, "Filtered:")) |
        halver() |  # 1, 4, 17, 72, ...
        utils.observe(printer=partial(print, "Halved:  ")) |
        itertools.islice(10)  # limits output to 10 items
    )
    print("Pipeline prepared:", pipeline)  # pipelines are lazily evaluated
    print("Sum of first 10 halved even fibonacci numbers:", sum(pipeline))


if __name__ == "__main__":
    main()
```
