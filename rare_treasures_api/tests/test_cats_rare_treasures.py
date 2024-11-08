'''This module contains the test suite for the `Cat's Rare Treasures` FastAPI app.'''
from typing import Optional
from pytest import mark, fixture
from fastapi.testclient import TestClient
from rare_treasures_api.main import app
from rare_treasures_api.utils.fp_utils import get_values
from rare_treasures_api.db.run_seed import run_seed

if not (row_counts:= run_seed('test')):
    raise RuntimeError('Database seeding failed')

SHOPS_ROW_COUNT, TREASURES_ROW_COUNT = row_counts


@fixture(scope='class')
def test_client():
    ''' returns a test client for the FastAPI app '''
    yield TestClient(app)
    # clean up
    run_seed('test')

@fixture(scope='function')
def get_treasures(test_client):
    ''' returns the treasures data from the given url '''
    return lambda url: test_client.get(url).context['treasures']


@mark.describe('testing treasure route handlers')
class TestTreasuresRouteHandlers:
    '''Test suite for the treasure route handlers'''

    @mark.it('testing an initial healthcheck responds with a message and 200 OK')
    def test_health_check(self, test_client):
        ''' test that the healthcheck route responds with a message and 200 OK '''

        response = test_client.get('/api/healthcheck')

        assert response.status_code == 200
        assert response.json() == {
            'message': 'application is healthy'
        }


    @mark.it('testing correct types on the returned treasures data')
    @mark.parametrize('name, expected_type', [
            ('treasure_id', int),
            ('treasure_name', str),
            ('colour', Optional[str]),
            ('age', Optional[int]),
            ('cost_at_auction', Optional[float]),
            ('shop_name', Optional[str])
    ])
    def test_all_treasures(self, name, expected_type, test_client):
        ''' test that the returned treasures have the correct types '''

        response = test_client.get('/api/treasures')
        treasures = response.context['treasures']

        assert response.status_code == 200
        assert len(treasures) == TREASURES_ROW_COUNT

        for treasure in treasures:
            assert isinstance(treasure[name], expected_type)


    @mark.it('testing is sorted by default in ascending order by age')
    def test_sorted_by_age(self, get_treasures):
        ''' test that the treasures are sorted by age in ascending order '''

        treasures = get_treasures('/api/treasures')
        sort_by_age = get_values('age', replace_none=True, sub=float('inf'))
        sorted_treasures = sorted(treasures, key=sort_by_age)

        assert treasures == sorted_treasures


    @mark.it('testing is sortable by query parameter')
    @mark.parametrize('sort_by', ['age', 'treasure_name', 'cost_at_auction'])
    def test_sort_by_query(self, sort_by, get_treasures):
        ''' test that the treasures are sorted by the given query parameter '''

        treasures = get_treasures(f'/api/treasures?sort_by={sort_by}')
        sort_by_key = get_values(sort_by, replace_none=True, sub=float('inf'))
        assert treasures == sorted(treasures, key=sort_by_key)


    @mark.it(
        'testing that a given order will return the table in ascending or descending order'
    )
    def test_ordering(self, get_treasures):
        ''' test that the treasures are sorted in the correct order '''

        sort_by_age = get_values('age', replace_none=True, sub=float('inf'))

        treasures_desc = get_treasures('/api/treasures?order=desc')
        treasures_asc = get_treasures('/api/treasures?order=asc')

        assert treasures_desc == sorted(treasures_desc, reverse=True, key=sort_by_age)
        assert treasures_asc == sorted(treasures_asc, key=sort_by_age)


    @mark.it(
        'testing that a combination of sort_by and order returns the table in the correct order'
    )
    def test_sort_by_and_ordering(self, get_treasures):
        ''' test that the treasures are sorted in the correct order '''
        treasure_sorted_desc = get_treasures('/api/treasures?sort_by=treasure_name&order=desc')
        treasure_sorted_asc = get_treasures('/api/treasures?sort_by=cost_at_auction&order=asc')

        sort_by_treasure = get_values('treasure_name', replace_none=True, sub=float('inf'))
        sort_by_cost_at_auction = get_values('cost_at_auction', replace_none=True, sub=float('inf'))

        assert treasure_sorted_desc == sorted(treasure_sorted_desc, reverse=True, key=sort_by_treasure)
        assert treasure_sorted_asc == sorted(treasure_sorted_asc, key=sort_by_cost_at_auction)


    @mark.it('testing redirects with error 400 when given an invalid sort_by query parameter')
    def test_invalid_sort_query(self, test_client):
        ''' test that the treasures are sorted by the given query parameter '''

        response_1 = test_client.get('/api/treasures?sort_by=abc_abc').context
        response_2 = test_client.get('/api/treasures?sort_by=id=1 OR 1=1').context

        assert response_1['status_code'] == 400
        assert response_1['message'] == '400 Bad Request: invalid query parameters'

        assert response_2['status_code'] == 400
        assert response_2['message'] == '400 Bad Request: invalid query parameters'


    @mark.it('testing responds with certain colour only')
    def test_filter_by_colour(self, get_treasures):
        ''' test that the treasures are filtered by colour '''
        treasures = get_treasures('/api/treasures?colour=gold')
        assert all(treasure['colour'] == 'gold' for treasure in treasures)


    @mark.it(
        'test inserts row into database and returns the newly inserted row in dict format'
    )
    def test_insert_treasure(self, test_client):
        ''' test that a new treasure can be inserted into the database '''

        row_1_to_insert = {
            'treasure_name': 'The Golden Fleece',
            'colour': 'gold',
            'age': 1000,
            'cost_at_auction': 1000000.00,
            'shop_id': 5
        }

        # test for optional empty fields
        row_2_to_insert = {'treasure_name': 'The Silver Chalice'}

        response_1 = test_client.post('/api/treasures', json=row_1_to_insert)
        response_2 = test_client.post('/api/treasures', json=row_2_to_insert)

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        assert response_1.json() == {
            'treasure_id': TREASURES_ROW_COUNT + 1,
            **row_1_to_insert
        }

        assert response_2.json() == {
            'treasure_id': TREASURES_ROW_COUNT + 2,
            'treasure_name': 'The Silver Chalice',
            'colour': None,
            'age': None,
            'cost_at_auction': None,
            'shop_id': None
        }
