''' General utility functions '''
from typing import Any

type RowsType = list[dict[str, Any]]

__all__: list[str] = ['format_response', 'flatten']


def format_response(columns, rows) -> RowsType:
    ''' format the rows returned from PG8000 query '''
    col_names: list[str] = [col['name'] for col in columns]
    formatted: RowsType = []

    if rows:
        formatted = [dict(zip(col_names, row)) for row in rows]

    return formatted


def get_column_names(cursor) -> list:
    '''Get column names from cursor description'''
    return [desc[0] for desc in cursor.description]


def flatten(lst: list[Any] | dict | tuple, depth=float('Inf')) -> list:
    '''
        flatten:
        flattens a nested list recursively to a given depth
        e.g. flatten([1, [2, 3, [4, 5]]], 2) -> [1, 2, 3, 4, 5]
        if depth is ommited, flattens completely
    '''
    if not list or depth < 1:
        return [lst] if not isinstance(lst, list) else lst

    flattend: list[Any] = []

    for v in lst:
        flattend += flatten(v, depth-1) if isinstance(v,(list, dict, tuple)) else [v]

    return flattend
