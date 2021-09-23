import inspect
from typing import Callable, Any, List, Tuple, Dict


def print_signature(function: Callable) -> None:
    print(inspect.signature(function))


def check_equality(annotation: Any, value: Any) -> bool:
    # probably won't deal with nested lists/tuples, rectify with recursive call
    if annotation == List:
        if not isinstance(value, list):
            return False
        for element in value:
            if type(element) not in annotation.__args__:
                return False

    elif annotation == Tuple:
        if not isinstance(value, tuple):
            return False
        if len(value) != len(annotation.__args__):
            return False
        for index, element in enumerate(value):
            if type(element) != annotation.__args__[index]:
                return False
    
    elif annotation == Dict:
        pass  # check key and value are of correct type
    
    else:
        if type(value) != annotation:
            return False
    
    return True
    


def type_check(function: Callable) -> Callable:
    signature = inspect.signature(function)
    return_annotation = signature.return_annotation

    def wrapper(*args, **kwargs) -> Any:
        for index, param in enumerate(signature.parameters.values()):
            if param.annotation == inspect.Parameter.empty:
                continue

            value = args[index] if index < len(args) else kwargs[param.name]
            if not check_equality(param.annotation, value):
                raise TypeError(f"Expected {param.annotation} for parameter {param.name}, got {type(args[index])} instead")

        result = function(*args, **kwargs)
        if return_annotation != inspect.Signature.empty:
            if return_annotation is None and result is None:
                pass
            elif not check_equality(return_annotation, result):
                raise TypeError(f"Expected {return_annotation} as return value, got {type(result)} instead")
        return result
    
    return wrapper