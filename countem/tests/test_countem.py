''' Test suite for the Countem module '''
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from pytest import mark
from countem import Countem


def format_ids(param):
    return f' {repr(param)} '.replace(' {', '> {')


@mark.describe('Tests for Countem class')
class TestCountem:

    @mark.it('when instantiated with no arguments returns an instance of Countem with no items')
    def test_with_empty_list(self):
        result = Countem()
        assert isinstance(result, Countem)
        assert not result

    @mark.describe('returns the correct counts for iterables')
    @mark.parametrize('iterable, expected',
        [
            (['a','b','c'], {'a': 1, 'b': 1, 'c': 1}),
            (['a','b','c','b'], {'a': 1, 'b': 2, 'c': 1}),
            ('apple', {'a': 1, 'p': 2, 'l': 1, 'e': 1}),
            ((1,2,'a',2,2,'a',3,'b','a'), {1: 1, 2: 3, 'a': 3, 3: 1, 'b': 1})
        ],
        ids=format_ids
    )
    def test_counts_for_iterable(self, iterable, expected):
        assert Countem(iterable) == expected

    @mark.describe('returns the correct maximum count for iterables')
    @mark.parametrize('iterable, expected',
        [
            (['a','b','c'], 1),
            (['a','b','c','b'], 2),
            ('apple', 2),
            ((1,2,'a',2,2,'a',3,'b','a'), 3),
            ([], None),
            ('', None)
        ],
        ids=format_ids
    )
    def test_maximum_of_iterable(self, iterable, expected):
        assert Countem(iterable).max() == expected


    @mark.describe('returns the correct modes for iterables')
    @mark.parametrize('iterable, expected',
        [
            (['a','b','c','a','b'], ('a','b')),
            ([1,5,2,1,2,5,2,5,5], (5,)),
            ([], None),
            ([0], (0,))
        ],
        ids=format_ids
    )
    def test_modes_of_iterable(self, iterable, expected):
        assert Countem(iterable).multi_mode() == expected

    @mark.describe('returns the correct update(addition) for iterables')
    @mark.parametrize('iterable, other, expected',
        [
            ([], 'abc', {'a': 1, 'b': 1, 'c': 1}),
            ([], 'abcabcabc', {'a': 3, 'b': 3, 'c': 3}),
            ({'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': -4, 'c': 3}, {'a': 3, 'b': -2, 'c': 6}),
            ([1, 2, 3], [1, 2, 3, 1, 2, 3], {1: 3, 2: 3, 3: 3})
        ],
        ids=format_ids
    )
    def test_update_of_iterable(self, iterable, other, expected):
        counted = Countem(iterable)

        assert counted + other == expected
        assert counted + Countem(other) == expected

        # update inplace
        counted.update(other)
        assert counted == expected



    @mark.describe('returns the correct subtractions for iterables')
    @mark.parametrize('iterable, other, expected',
        [
            ([], 'abc', {'a': -1, 'b': -1, 'c': -1}),
            ([], 'abcabcabc', {'a': -3, 'b': -3, 'c': -3}),
            ({'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': -4, 'c': 3}, {'a': -1, 'b': 6, 'c': 0}),
            ([1, 2, 3], [1, 2, 3, 1, 2, 3], {1: -1, 2: -1, 3: -1})
        ],
        ids=format_ids
    )
    def test_subtraction_of_iterable(self, iterable, other, expected):
        counted = Countem(iterable)

        assert counted - other == expected
        assert counted - Countem(other) == expected

        # subtract inplace
        counted.subtract(other)
        assert counted == expected
