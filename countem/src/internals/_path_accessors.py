""" Internal module for path accessors """

from typing import Callable, Union, List, Dict, Any

__all__ = ['get_by_path']


def get_by_path(*path, default=None) -> Callable:
    '''
    gets a nested property value following a given path

    e.g.    get_by_path('pet', 'age')(user)
            equivalent to `'pet' in user and user['pet'].get('age', default)`

    get_by_path(path, obj, default(optional))

    Params:
        path: a series of string keys or index values that make a path.
        default: optional value to return if key is not found — default is None

    Returns: a function to call on a given object
    '''
    def get_by_path_from(obj: Union[Dict, List]) -> Any:
        '''
        Params:
            obj: a list or dictionary to find a value on using the path
        '''
        value = obj

        for key in path:
            try:
                value = value[key]
            except (KeyError, IndexError, TypeError):
                return default

        return value

    return get_by_path_from
