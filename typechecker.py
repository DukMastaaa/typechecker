import inspect
from typing import get_origin, get_args, Callable, Any, Literal, Tuple, Union, List


def print_signature(function: Callable) -> None:
    print(inspect.signature(function))


_RECOGNISED_CONTAINER_TYPES = [tuple, list, dict, set]


# I need to modify this after `check_equality` is defined because
# the functions in here reference `check_equality`
_TYPING_MODULE_DISPATCH_TABLE = dict()  # for annotations from the `typing` module
_MISC_DISPATCH_TABLE = dict()  # for miscellaneous types not from `typing`


def check_equality(value: Any, annotation: Any) -> bool:
    # requires python >= 3.8
    # https://docs.python.org/3/library/typing.html#typing.get_origin
    # annotations from `typing` are now deprecated for python >= 3.9 but still works ._.
    
    origin = get_origin(annotation)
    annotation_args = get_args(annotation)
    
    if origin is not None:
        if origin in _RECOGNISED_CONTAINER_TYPES:
            if not isinstance(value, origin):
                return False
            elif len(annotation_args) == 0:
                return True
        return _TYPING_MODULE_DISPATCH_TABLE[origin](value, annotation_args)
    else:
        try:
            return _MISC_DISPATCH_TABLE[annotation](value, annotation)
        except KeyError:
            return isinstance(value, annotation)


def _handle_list(value: list, annotation_args: Tuple[Any]) -> bool:
    if len(value) == 0:
        return True
    return all(check_equality(element, annotation_args[0]) for element in value)


def _handle_tuple(value: tuple, annotation_args: Tuple[Any, ...]) -> bool:
    if len(value) != len(annotation_args):
        return False
    return all(
        check_equality(element, element_type)
        for element, element_type in zip(value, annotation_args)
    )


def _handle_dict(value: dict, annotation_args: Tuple[Any, Any]) -> bool:
    if len(value) == 0:
        return True
    key_annotation, value_annotation = annotation_args
    return all(check_equality(key, key_annotation) for key in value.keys()) \
        and all(check_equality(val, value_annotation) for val in value.values())


def _handle_set(value: set, annotation_args: Tuple[Any]) -> bool:
    # behaviour same
    return _handle_list(value, annotation_args)


def _handle_union(value: Any, annotation_args: Tuple[Any, ...]) -> bool:
    return any(check_equality(value, annotation_type) for annotation_type in annotation_args)


def _handle_literal(value: Any, annotation_args: Tuple[Any, ...]) -> bool:
    return any(value == literal_element for literal_element in annotation_args)


def _handle_any(value: Any, annotation_args: Tuple) -> bool:
    return True


def _handle_ellipsis(value: Any, annotation: Any) -> bool:
    """Used for the ellipsis literal `...`"""
    return value == ...


_TYPING_MODULE_DISPATCH_TABLE.update({
    list: _handle_list,
    tuple: _handle_tuple,
    dict: _handle_dict,
    set: _handle_set,
    Union: _handle_union,
    Literal: _handle_literal,
    Any: _handle_any
})


_MISC_DISPATCH_TABLE.update({
    ...: _handle_ellipsis
})


def type_check(function: Callable) -> Callable:
    signature = inspect.signature(function)
    return_annotation = signature.return_annotation

    def wrapper(*args, **kwargs) -> Any:
        for index, param in enumerate(signature.parameters.values()):
            if param.annotation == inspect.Parameter.empty:
                continue

            value = args[index] if index < len(args) else kwargs[param.name]
            if not check_equality(value, param.annotation):
                raise TypeError(f"Expected {param.annotation} for parameter {param.name}, got {type(value)} instead")

        result = function(*args, **kwargs)
        if return_annotation != inspect.Signature.empty:
            if return_annotation is None and result is None:
                pass
            elif not check_equality(result, return_annotation):
                raise TypeError(f"Expected {return_annotation} as return value, got {type(result)} instead")
        return result
    
    return wrapper
