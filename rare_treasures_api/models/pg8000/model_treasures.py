''' models and functions for treasures table '''

from typing import Literal, Optional, Any
from pydantic import BaseModel, field_validator
from fastapi import HTTPException
from ...db.pg8000.connection import CreateConnection
from ...utils import format_response, flatten

__all__: list[str] = [
    'fetch_colours',
    'fetch_shop_names',
    'fetch_treasures',
    'insert_treasure',
    'Treasure',
    'TreasureQueryParams'
]

# define type aliases
type RowsType = list[list[Any]] | None

class Treasure(BaseModel):
    ''' model for treasure '''
    treasure_name: str
    colour: str
    age: int
    cost_at_auction: float
    shop_name: str


class TreasureQueryParams(BaseModel):
    ''' model for treasure query parameters '''

    sort_by: Literal['treasure_name', 'age', 'cost_at_auction'] = 'age'
    order: Literal['asc', 'desc'] = 'asc'
    colour: Optional[str] = None

    @field_validator('colour')
    @classmethod
    def validate_colour(cls, colour: str) -> str:
        ''' checks the given colour against available colours '''
        if not colour:
            return 'NULL'

        if colour in fetch_colours():
            return colour

        raise HTTPException(
            status_code=422, detail='Unprocessable Content: cannot filter colours with given key'
        )


def fetch_colours() -> list[str]:
    ''' fetches all coiours used in the treasures table '''
    with CreateConnection() as conn:
        response: RowsType = conn.run('SELECT DISTINCT colour FROM treasures')
        return flatten(response) if response else []


def fetch_shop_names() -> list[str]:
    ''' fetches all shop names in the shops table '''
    with CreateConnection() as conn:
        response: RowsType = conn.run('SELECT shop_name FROM shops')
        return flatten(response) if response else []


def fetch_treasures(params: TreasureQueryParams) -> dict[str, Any]:
    ''' fetches rows from treasure table with a given key to sort by '''

    sql = f"""
    SELECT
        treasure_id, treasure_name, colour, age, cost_at_auction, shop_name
    FROM treasures
    JOIN shops USING(shop_id)
    WHERE (colour = :colour or :colour = 'NULL')
    ORDER BY {params.sort_by} {params.order};
    """

    with CreateConnection() as conn:
        rows: RowsType = conn.run(sql, colour=params.colour)
        if isinstance(rows, list):
            return {'treasures': format_response(conn.columns, rows)}
        return {}


def insert_treasure(props: Treasure) -> dict[str, Any]:
    ''' add a new entry to the treasure table '''
    dict_props: dict[str, Any] = props.model_dump()

    sql = (
        """
        INSERT INTO treasures
            (treasure_name, colour, age, cost_at_auction, shop_id)
        VALUES
            (:treasure_name, :colour, :age, :cost_at_auction, :shop_id)
        RETURNING *;
        """
    )

    with CreateConnection() as conn:
        if not (response:= conn.run('SELECT shop_name, shop_id FROM shops')):
            return {}

        shop_ids = dict(response)

        if (shop_id := shop_ids.get(props.shop_name)):
            rows: RowsType = conn.run(sql, shop_id=shop_id, **dict_props)

            if isinstance(rows, list):
                return format_response(conn.columns, rows)[0]

        return {}
