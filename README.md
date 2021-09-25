# typechecker

Python tool which aims to enforce "static" typing in function calls by parsing function signatures.
The `typechecker` module provides a `type_check` decorator, used like:
```python
@type_check
def add(x: int, y: int) -> int:
    return x + y
```
which will make `add` throw `TypeError` if input/output types are different than what's indicated.
See `main.py` for more examples.
