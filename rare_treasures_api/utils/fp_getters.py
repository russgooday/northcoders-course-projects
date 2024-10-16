''' Functional programming utilities for getting props from objects '''
from typing import Dict, Tuple, Callable

__all__ = ['pick_props', 'get_values']


def pick_props(*keys) -> Callable:
    ''' returns selected props from a given object '''
    def _pick(obj: Dict) -> Dict:
        return {key: obj[key] for key in keys}
    return _pick


def get_values(*keys) -> Callable:
    ''' returns selected props from a given object '''
    def _get_values(obj: Dict) -> Tuple:
        if len(keys) == 1:
            return obj[keys[0]]
        return tuple(obj[key] for key in keys)
    return _get_values
