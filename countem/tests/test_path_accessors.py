'''This module contains the test suite for path accessor helper functions.'''
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import re
from pytest import mark
from countem.src import get_by_path

# Test cases for get_by_path
test_cases_get_by_path = [
    # Test case 1
    (['a','b','c'], {'a': {'b': {'c': 1}}}, 1),
    # Test case 2
    (['a','b'], {'a': {'b': {'c': 1}}}, {'c': 1}),
    # Test case 3
    (['a','b','c'], {'a': 1}, None),
    # Test case 4
    (['a','b','c'], {'a': {'b': 2}}, None),
    # Mix of lists and dicts
    (['a',1,'c'], {'a': [{}, {'c': 1}]}, 1),
    # Various key types
    ([True, 1.5, 0, 'x'], {True: {1.5: {0: {'x': 2}}}}, 2)
]

@mark.describe('Tests for get_by_path')
class TestFindMostRepeated:

    @mark.it('when passed a path returns a function')
    def test_returns_function(self):
        assert callable(get_by_path('dummy', 'path'))


    @mark.it('when passed an empty path or and empty object returns the default value')
    def test_returns_a_default_value(self):
        assert not get_by_path('')({'x': 2})
        assert get_by_path('', default='not found!')({'x': 2}) == 'not found!'
        assert get_by_path('x', default='not found!')({}) == 'not found!'


    @mark.it("given a path, returns the correct value")
    @mark.parametrize(
        'path, obj, expected',
        test_cases_get_by_path,
        ids=[re.sub(r'(?<=[\]\}]),', ' ->', str(test)) for test in test_cases_get_by_path]
    )
    def test_returns_the_correct_property(self, path, obj, expected):
        assert get_by_path(*path)(obj) == expected
