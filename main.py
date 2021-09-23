from typechecker import type_check
from typing import List


@type_check
def add(x: int, y: int) -> int:
    return x + y


class Foo:
    def __init__(self, x: int) -> None:
        self.x: int = x
        self.y: int = 123


@type_check
def meow(f: Foo, i: int) -> None:
    f.x += i


@type_check
def beans(numbers: List[int], multiplier: int) -> List[int]:
    return [multiplier * num for num in numbers]


if __name__ == "__main__":
    print(add(1, 2))
    foo = Foo(1)
    print(meow(foo, 100))

    # numbers = [1, 2, 3, 4, 5]
    # print(beans(numbers, 5))
