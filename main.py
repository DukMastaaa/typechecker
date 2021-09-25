from typechecker import type_check
from typing import List, Dict, Tuple


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


@type_check
def sum_of_even_keys(d: Dict[int, int]) -> int:
    return sum(value for key, value in d.items() if key % 2 == 0)


@type_check
def add_2d_vectors(vectors: List[Tuple[int, int]]) -> Tuple[int, int]:
    return (sum(vec[0] for vec in vectors), sum(vec[1] for vec in vectors))


if __name__ == "__main__":
    # print(add(1, 2))
    # foo = Foo(1)
    # print(meow(foo, 100))

    # numbers = [1, 2, 3, 4, 5]
    # print(beans(numbers, 5))

    # d = {1: 1, 2: 5, 3: 9, 4: 11}
    # print(sum_of_even_keys(d))

    print(add_2d_vectors([(1, 2), (2, 4), (3, 6), (4, 8)]))
