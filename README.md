# typechecker

Python tool which aims to enforce "static" typing in function calls by parsing function signatures.
The `typechecker` module provides a `type_check` decorator, used like:
```python
@type_check
def add(x: int, y: int) -> int:
    return x + y
```
which will make `add` throw `TypeError` if input/output types are different than what's indicated.

A more advanced example involving nested annotations:
```python
@type_check
def add_2d_vectors(vectors: List[Tuple[int, int]]) -> Tuple[int, int]:
    return (sum(vec[0] for vec in vectors), sum(vec[1] for vec in vectors))

print(add_2d_vectors([(1, 2), (2, 4), (3, 6), (4, 8)]))
>>> (10, 20)
```
See `main.py` for more examples.
