import json
from .connection import CreateConnection
from ..dependencies import root_dir
from .tables_sql import (
    DROP_TABLES, 
    SHOPS_SCHEMA, 
    TREASURES_SCHEMA, 
    POPULATE_SHOPS, 
    POPULATE_TREASURES
)

def seed_db(env='test'):
    print('\U0001FAB4', 'Seeding Database...')

    with CreateConnection() as db:
        shops_path = f'{root_dir}/data/{env}-data/shops.json'
        treasures_path = f'{root_dir}/data/{env}-data/treasures.json'

        db.run(DROP_TABLES)
        db.run(SHOPS_SCHEMA)
        db.run(TREASURES_SCHEMA)

        with open(shops_path, 'r', encoding='utf-8') as file:
            rows = json.load(file)['shops']
            row_count = 0

            for row in rows:
                db.run(
                    POPULATE_SHOPS, 
                    shop_name=row['shop_name'],
                    owner=row['owner'],
                    slogan=row['slogan']
                )
                row_count += 1

            print(f'Successfully seeded {row_count} rows to `shops` table in the database.')

        shops = db.run('SELECT * FROM shops')
        shop_ids = {shop[1]: shop[0] for shop in shops}

        with open(treasures_path, 'r', encoding='utf-8') as file:
            rows = json.load(file)['treasures']
            row_count = 0

            for row in rows:
                db.run(
                    POPULATE_TREASURES,
                    treasure_name=row.get('treasure_name'),
                    colour=row.get('colour'),
                    age=row.get('age'),
                    cost_at_auction=row.get('cost_at_auction'),
                    shop_id=shop_ids.get(row['shop'])
                )
                row_count += 1

            print(f'Successfully seeded {row_count} rows to `treasures` table in the database. \U0001F44D')


