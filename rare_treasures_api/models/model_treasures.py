''' models and functions for treasures table '''

from typing import Literal, Optional, Any
import pandas as pd
from pydantic import BaseModel, field_validator, PositiveInt
from fastapi import HTTPException
from sqlalchemy import select, insert, desc, asc
from ..db.connection import create_connection
from ..db.tables_classes import Treasures, Shops


__all__: list[str] = [
    'fetch_colours',
    'fetch_shop_names',
    'fetch_treasures',
    'insert_treasure',
    'TreasureFields',
    'TreasureQueryParams'
]


class TreasureFields(BaseModel):
    ''' model for treasure '''
    treasure_name: str
    colour: Optional[str] = None
    age: Optional[int] = None
    cost_at_auction: Optional[float] = None
    shop_id: Optional[int] = None


class TreasureQueryParams(BaseModel):
    ''' validation model for treasure query parameters '''
    sort_by: Literal['treasure_name', 'age', 'cost_at_auction'] = 'age'
    order: Literal['asc', 'desc'] = 'asc'
    colour: Optional[str] = None
    page: PositiveInt = 1

    @field_validator('colour')
    @classmethod
    def validate_colour(cls, colour: str) -> str | None:
        ''' checks the given colour against available colours '''
        if not colour:
            return None

        if colour in fetch_colours():
            return colour

        raise HTTPException(
            status_code=422,
            detail='Unprocessable Content: cannot filter colours with given key'
        )


def fetch_column(conn, column, distinct: bool=False) -> list[str]:
    ''' fetches all distinct values in a column '''
    stmt = select(column).where(column.is_not(None))
    response = conn.execute(stmt.distinct() if distinct else stmt)
    return list(response.scalars().all())


def fetch_colours() -> list[str]:
    ''' fetches all coiours used in the treasures table '''
    if not (conn:= create_connection()):
        return []

    with conn.begin():
        return fetch_column(conn, Treasures.colour, distinct=True)


def fetch_shop_names() -> list[str]:
    ''' fetches all shop names in the shops table '''
    if not (conn:= create_connection()):
        return []

    with conn.begin():
        return fetch_column(conn, Shops.shop_name, distinct=True)


def fetch_treasures(params: TreasureQueryParams) -> dict[str, list[dict]]:
    """ fetches rows from treasure table using given keys to sort and filter by

    Args:
        params (TreasureFields): Parameters to sort and filter by

        params.sort_by (str): The column to sort by
        params.order (str): 'asc' or 'desc' The order to sort by
        params.colour (str | None): The colour to filter by, if None, no filter is applied

    Returns:
        type (dict[str, list[dict]]): A dictionary of treasures with the following structure:
        {
            'treasures': [
                {
                    'treasure_name': str,
                    'colour': str,
                    'age': int,
                    'cost_at_auction': float(2),
                    'shop_name': str
                },
                ...
            ]
        }
    """
    if not (conn:= create_connection()):
        return {}

    sort_dir = desc if params.order == 'desc' else asc
    # table aliases
    t = Treasures
    s = Shops

    with conn.begin():
        # TODO: implement pagination with limit and offset
        stmt = (
            select(
                t.treasure_id,
                t.treasure_name,
                t.colour,
                t.age,
                t.cost_at_auction,
                s.shop_name
            )
            .outerjoin(s) # LEFT OUTER JOIN, include treasures without shop_ids
            .order_by(sort_dir(params.sort_by))
        )

        if params.colour:
            stmt = stmt.filter(t.colour == params.colour)

        column_names = stmt.selected_columns.keys()
        rows = conn.execute(stmt).all()
        pd_treasures = (pd.DataFrame(rows, columns=column_names).convert_dtypes(dtype_backend='pyarrow'))

        return {'treasures': pd_treasures.to_dict('records')}


def insert_treasure(params: TreasureFields) -> dict[str, Any]:
    """ insert a row into the treasures table

    Args: params (TreasureFields): Parameters values to insert

        params.treasure_name: str
        Optional:
        params.colour: str
        params.age: int
        params.cost_at_auction: float
        params.shop_id: int

    Returns:
        type (dict[str, Any]): A dictionary of inserted row with the following structure:
            {
                'treasure_id': int,
                'treasure_name': str,
                'colour': str,
                'age': int,
                'cost_at_auction': float(2),
                'shop_id': int
            }
    """
    if not (conn:= create_connection()):
        return {}

    with conn.begin():
        t = Treasures
        params_dict = params.model_dump()
        stmt = (
            insert(t)
            .values(params_dict)
            .returning(*t.__table__.c)
        )

        result = conn.execute(stmt)
    # return the inserted row as a dictionary
    return dict(result.mappings().one())
