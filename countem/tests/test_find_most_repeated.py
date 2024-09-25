'''This module contains the test suite for the find_most_repeated function.'''
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from pytest import mark
from countem.src.find_most_repeated import find_most_repeated


@mark.describe('Tests for find most repeated function')
class TestFindMostRepeated:

    @mark.it('when passed an empty list returns the default dictionary')
    def test_with_empty_list(self):
        assert find_most_repeated([]) == {'elements': [], 'repeats': None}


    @mark.it(
        'when passed a list of non repeating elements returns the default dictionary'
    )
    def test_with_unique_elements(self):
        assert find_most_repeated(['a','b','c']) == {'elements': [], 'repeats': None}


    @mark.it(
        '''
        when passed a list containing a single duplicate will return that item in elements
        with a repeat count of two
        '''
    )
    def test_with_single_duplicate(self):
        assert find_most_repeated(['a','b','b','c']) == {'elements': ['b'], 'repeats': 2}


    @mark.it(
        '''
        will add multiple elements to the list if they share the same amount of
        maximum repetitions
        '''
    )
    def test_with_multiple_repetitions(self):
        elements = ['a', 'b', 'b', 3, 'c', 3, 'c', 3, 'b']
        assert find_most_repeated(elements) == {'elements': ['b', 3], 'repeats': 3}
