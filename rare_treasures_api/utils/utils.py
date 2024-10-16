''' General utility functions '''
from typing import Union, List, Dict
import re

__all__ = ['format_response', 'flatten']

SNAKE_CASE = re.compile(r'^[a-z][a-z0-9]*$|^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$', flags=re.I)

def format_response(columns, rows, label:str = '') -> Union[List, Dict]:
    ''' format the rows returned from PG8000 query '''
    col_names = [col['name'] for col in columns]
    formatted = []

    if rows:
        formatted = [dict(zip(col_names, row)) for row in rows]

    return { label: formatted } if label else formatted


def create_insert_values(props: Dict, prefix: str='') -> str:
    ''' creates comma separated placeholders from key names '''
    return ', '.join(f'{prefix}{k}' for k in props)


def create_set_placeholders(props: Dict) -> str:
    ''' creates comma separated placeholders from key names '''
    return ', '.join(f'{k} = :{k}' for k in props)


def flatten(lst: list|dict|tuple, depth=float('Inf')) -> List:
    '''
        flatten:
        flattens a nested list recursively to a given depth
        e.g. flatten([1, [2, 3, [4, 5]]], 2) -> [1, 2, 3, 4, 5]
        if depth is ommited, flattens completely
    '''
    if not list or depth < 1:
        return lst

    flattend = []

    for v in lst:
        flattend += flatten(v, depth-1) if isinstance(v, (list, dict, tuple)) else [v]

    return flattend


def is_snake_case(string:str) -> bool:
    ''' checks if a string matches snake_case and returns a boolean '''
    return bool(SNAKE_CASE.match(string))
