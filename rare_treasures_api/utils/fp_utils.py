''' Functional programming utilities '''
from typing import Dict, Callable

__all__ = ['pick_props', 'get_values']


def pick_props(*keys) -> Callable:
    ''' returns selected props from a given object '''
    def _pick(obj: Dict) -> Dict:
        return {key: obj[key] for key in keys}
    return _pick


def get_values(*keys, replace_none: bool = False, sub = None) -> Callable:
    ''' returns selected props from a given object '''
    def _get_values(obj: Dict):

        if replace_none:
            if len(keys) == 1:
                if (val:= obj.get(keys[0])) is None:
                    return sub
                return val
            return tuple(sub if (val:= obj.get(key)) is None else val for key in keys)

        if len(keys) == 1:
            return obj.get(keys[0], None)
        return tuple(obj.get(key, sub) for key in keys)

    return _get_values
