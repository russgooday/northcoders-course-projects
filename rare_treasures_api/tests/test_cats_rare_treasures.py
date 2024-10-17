'''This module contains the test suite for the `Cat's Rare Treasures` FastAPI app.'''
from pytest import mark, fixture
from fastapi.testclient import TestClient
from rare_treasures_api.main import app
from rare_treasures_api.utils.fp_getters import get_values
# from db.seed import seed_db

@fixture(scope='function')
def test_client():
    return TestClient(app)


@fixture(scope='function')
def get_treasures(test_client):
    return lambda url: test_client.get(url).context['treasures']


@mark.describe('testing treasure route handlers')
class TestTreasuresRouteHandlers:

    @mark.it('testing an initial healthcheck responds with a message and 200 OK')
    def test_health_check(self, test_client):
        response = test_client.get('/api/healthcheck')

        assert response.status_code == 200
        assert response.json() == {
            'message': 'application is healthy'
        }


    @mark.it('testing correct types on the returned treasures data')
    @mark.parametrize('sort_by, expected_type', [
            ('treasure_id', int),
            ('treasure_name', str),
            ('colour', str),
            ('age', int),
            ('cost_at_auction', float),
            ('shop_name', str)
    ])
    def test_all_treasures(self, sort_by, expected_type, test_client):
        response = test_client.get('/api/treasures')
        treasures = response.context['treasures']

        assert response.status_code == 200
        assert len(treasures) == 26

        for treasure in treasures:
            assert isinstance(treasure[sort_by], expected_type)


    @mark.it('testing is sorted by default in ascending order by age')
    def test_sorted_by_age(self, get_treasures):
        treasures = get_treasures('/api/treasures')

        assert treasures == sorted(treasures, key=get_values('age'))


    @mark.it('testing is sortable by query parameter')
    @mark.parametrize('sort_by', ['age', 'treasure_name', 'cost_at_auction'])
    def test_sort_by_query(self, sort_by, get_treasures):
        treasures = get_treasures(f'/api/treasures?sort_by={sort_by}')

        assert treasures == sorted(treasures, key=get_values(sort_by))


    @mark.it(
        'testing that a given order will return the table in ascending or descending order'
    )
    def test_ordering(self, get_treasures):
        age = get_values('age')

        treasures_desc = get_treasures('/api/treasures?order=desc')
        treasures_asc = get_treasures('/api/treasures?order=asc')

        assert treasures_desc == sorted(treasures_desc, reverse=True, key=age)
        assert treasures_asc == sorted(treasures_asc, key=age)


    @mark.it(
        'testing that a combination of sort_by and order returns the table in the correct order'
    )
    def test_sort_by_and_ordering(self, get_treasures):
        treasure_sorted_desc = get_treasures('/api/treasures?sort_by=treasure_name&order=desc')
        treasure_sorted_asc = get_treasures('/api/treasures?sort_by=cost_at_auction&order=asc')

        assert treasure_sorted_desc == sorted(treasure_sorted_desc, reverse=True, key=get_values('treasure_name'))
        assert treasure_sorted_asc == sorted(treasure_sorted_asc, key=get_values('cost_at_auction'))


    @mark.it('testing redirects with error 400 when given an invalid sort_by query parameter')
    def test_invalid_sort_query(self, test_client):
        response_1 = test_client.get('/api/treasures?sort_by=abc_abc').context
        response_2 = test_client.get('/api/treasures?sort_by=id=1 OR 1=1').context

        assert response_1['status_code'] == 400
        assert response_1['message'] == '400 Bad Request: invalid query parameters'

        assert response_2['status_code'] == 400
        assert response_2['message'] == '400 Bad Request: invalid query parameters'


    @mark.it('testing responds with certain colour only')
    def test_filter_by_colour(self, get_treasures):
        ''' test that the treasures are filtered by colour '''
        treasures = get_treasures('/api/treasures?colour=onyx')

        assert all(treasure['colour'] == 'onyx' for treasure in treasures)
