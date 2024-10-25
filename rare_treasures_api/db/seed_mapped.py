'''
Description: Seeds the database using SQLAlchemy ORM.
Table inserts are compiled first for bulk insertion.
In tests this is 10x faster than Raw SQL interative inserts.
Pandas is used to process the JSON files for parameters.
'''
import pandas as pd
from sqlalchemy import insert
from .connection import engine, create_session
from ..dependencies import ROOT_PATH
from ..utils.file_utils import load_json_data
from .tables_classes import (Base, Shops, Treasures)


def fetch_shops(shops_path: str) -> pd.DataFrame:
    '''load and prepare shops table'''
    shops_json = load_json_data(shops_path)['shops']

    # create a dataframe and process the data
    shops_df = pd.DataFrame(shops_json, dtype='string')
    shops_df['shop_id'] = pd.RangeIndex(1, len(shops_json) + 1)

    return shops_df.convert_dtypes(dtype_backend='pyarrow')


def fetch_treasures(treasures_path: str, shops_df: pd.DataFrame) -> pd.DataFrame:
    '''load and prepare treasures table'''
    treasures_json = load_json_data(treasures_path)['treasures']

    # create a dataframe and process the data
    treasures_df = pd.DataFrame(treasures_json)
    # get the shop_ids by 'shop_name' from shops and build a 'shop_id' column for treasures
    # the getter on shop's 'shop_id' column can be used as a callback to achieve this
    shop_ids = pd.Series(shops_df['shop_id'].values, index=shops_df['shop_name'])
    treasures_df['shop_id'] = treasures_df['shop'].apply(shop_ids.get)
    treasures_df.drop(columns='shop', inplace=True)

    return treasures_df.convert_dtypes(dtype_backend='pyarrow')


def seed_db(env: str = 'test') -> tuple[int, int] | None:
    '''Seed the database using SQLAlchemy ORM
        Args:
            env (str): the environment 'test' or 'dev' to seed the database with
        Returns:
            tuple[int, int] | None: a tuple of the inserted row counts
            (shops.row_count, treasures.row_count)
            or None if seeding failed
    '''

    print('Seeding Database...\n')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    if not (session := create_session()):
        return None

    with session.begin():
        shops_path: str = f'{ROOT_PATH}/data/{env}-data/shops.json'
        treasures_path: str = f'{ROOT_PATH}/data/{env}-data/treasures.json'

        shops_df: pd.DataFrame = fetch_shops(shops_path)
        treasures_df: pd.DataFrame = fetch_treasures(treasures_path, shops_df)

        shops = session.execute(insert(Shops).values(shops_df.to_dict('records')))
        treasures = session.execute(insert(Treasures).values(treasures_df.to_dict('records')))
        print('treasures row count:', treasures.rowcount)

    print('Database seeded!')

    return ( shops.rowcount, treasures.rowcount )
