DROP_TABLES = '''
    DROP TABLE if exists treasures;
    DROP TABLE if exists shops;
'''

SHOPS_SCHEMA = '''
    CREATE TABLE shops (
        shop_id SERIAL PRIMARY KEY,
        shop_name VARCHAR(42) NOT NULL,
        owner VARCHAR(42),
        slogan VARCHAR (256)
    )
'''

TREASURES_SCHEMA = '''
    CREATE TABLE treasures (
        treasure_id SERIAL PRIMARY KEY,
        treasure_name VARCHAR(256) NOT NULL,
        colour VARCHAR (42),
        age INT,
        cost_at_auction FLOAT(2),
        shop_id INT REFERENCES shops(shop_id)
    )
'''

POPULATE_SHOPS = '''
    INSERT INTO shops (shop_name, owner, slogan)
    VALUES (:shop_name, :owner, :slogan)
'''

POPULATE_TREASURES = '''
    INSERT INTO treasures (treasure_name, colour, age, cost_at_auction, shop_id)
    VALUES (:treasure_name, :colour, :age, :cost_at_auction, :shop_id)
'''
