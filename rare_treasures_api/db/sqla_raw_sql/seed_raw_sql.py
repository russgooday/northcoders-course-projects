'''
Description: Seeds the database using SQL Alchemy and raw SQL.
Table insertion is done interactively and is considerably slower than the ORM.
Pandas is used to process the JSON files for parameters.
'''
from typing import Any
import pandas as pd
from sqlalchemy import text
from ..connection import create_session
from ...dependencies import ROOT_PATH
from ...utils.file_utils import load_json_data
from .tables_sql import (
    DROP_TABLES,
    SHOPS_SCHEMA,
    TREASURES_SCHEMA,
    POPULATE_SHOPS,
    POPULATE_TREASURES
)

# Note workaround: pandas df.to_dict() returns type list[dict[Hashable, Any]]
# this causes type checking issues with slqalchemy's insert
# which expects a type of list[dict[str, Any]]
def df_to_dicts(df: pd.DataFrame) -> list[dict[str, Any]]:
    '''Converts a DataFrame to a list of dictionaries'''
    return [row.to_dict() for _, row in df.iterrows()]


def fetch_shops(shops_path: str) -> pd.DataFrame:
    '''load and prepare shops table'''
    shops_json = load_json_data(shops_path)['shops']

    # create a dataframe and process the data
    shops_df = pd.DataFrame(shops_json)
    shops_df['shop_id'] = pd.RangeIndex(1, len(shops_json) + 1)

    return shops_df.convert_dtypes(dtype_backend='pyarrow')


def fetch_treasures(treasures_path: str, shops_df: pd.DataFrame) -> pd.DataFrame:
    '''load and prepare treasures table'''
    treasures_json = load_json_data(treasures_path)['treasures']

    # create a dataframe and process the data
    treasures_df = pd.DataFrame(treasures_json)

    # get the shop_ids by 'shop_name' from shops and build a 'shop_id' column for treasures
    # the getter on shop's 'shop_id' column can be used as a callback to achieve this
    shop_ids = shops_df.set_index('shop_name')['shop_id']
    treasures_df['shop_id'] = treasures_df['shop'].apply(shop_ids.get)

    return treasures_df.convert_dtypes(dtype_backend='pyarrow')


def seed_db(env:str = 'test') -> None:
    '''Seed the database'''
    print('Seeding Database...\n')

    if not (session := create_session()):
        return None

    with session.begin():
        shops_path = f'{ROOT_PATH}/data/{env}-data/shops.json'
        treasures_path = f'{ROOT_PATH}/data/{env}-data/treasures.json'

        session.execute(text(DROP_TABLES))
        session.execute(text(SHOPS_SCHEMA))
        session.execute(text(TREASURES_SCHEMA))

        shops_df = fetch_shops(shops_path)
        treasures_df = fetch_treasures(treasures_path, shops_df)

        # arguments for placeholders are passed in as a list of dictionaries
        session.execute(text(POPULATE_SHOPS), df_to_dicts(shops_df))
        session.execute(text(POPULATE_TREASURES), df_to_dicts(treasures_df))

    print('Database seeded!')

if __name__ == '__main__':
    seed_db('test')
