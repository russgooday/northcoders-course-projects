'''This module contains the logic to seed the development databases
for the `Cat's Rare Treasures` FastAPI app.'''
from .seed_mapped import seed_db

def run_seed(environment='test'):
    ''' Seed the development database '''
    try:
        return seed_db(environment)
    except Exception as e:
        print(e)
        raise e
