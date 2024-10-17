'''This module contains the logic to seed the development databases
for the `Cat's Rare Treasures` FastAPI app.'''
from .seed import seed_db

def run_seed(environment='test'):
    ''' Seed the development database '''
    try:
        seed_db(environment)
    except Exception as e:
        print(e)
        raise e
