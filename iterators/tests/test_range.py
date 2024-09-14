'''This module contains the test suite for the range function.'''
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from typing import Iterator
from pytest import mark, raises
from iterators.src import NCRange


@mark.describe('Series of tests for the NCRange Constructor')
class TestNCRangeConstructor:

    @mark.it(
        'when passed no arguments raises a ValueError'
    )
    def test_if_no_arguments(self):

        with raises(ValueError) as excinfo:
            NCRange()
        assert (
            'NCRange expected at least 1 argument, got 0' in str(excinfo.value)
        )


    @mark.it(
        'when passed anything other than integers raises TypeError'
    )
    def test_if_not_all_integer_arguments(self):

        with raises(TypeError) as excinfo:
            NCRange(None,1,2)
        assert (
            "'NoneType' object cannot be interpreted as an integer" in str(excinfo.value)
        )


    @mark.it(
        'when passed a step of zero raises a ValueError'
    )
    def test_if_step_is_zero(self):

        with raises(ValueError) as excinfo:
            NCRange(1,5,0)
        assert (
            'arg 3 must not be zero' in str(excinfo.value)
        )

    @mark.it(
        '''
        when passed one argument start is assigned zero and stop
        is assigned that argument value. step defaults to 1
        '''
    )
    def test_if_only_start_provided(self):
        iterator = NCRange(5)
        assert iterator.start == 0
        assert iterator.stop == 5
        assert iterator.step == 1


    @mark.it(
        '''
        when passed two arguments, start and stop are assigned those values respectively
        '''
    )
    def test_if_start_and_stop_provided(self):
        iterator = NCRange(1,5)
        assert iterator.start == 1
        assert iterator.stop == 5
        assert iterator.step == 1


    @mark.it(
        '''
        when passed a third optional argument, this will be assigned to step
        '''
    )
    def test_if_step_provided(self):
        iterator = NCRange(5,1,-1)
        assert iterator.start == 5
        assert iterator.stop == 1
        assert iterator.step == -1


@mark.describe('Series of tests for NCRange')
class TestNCRange:

    @mark.it("instance is iterable and can create an iterator")
    def test_creates_an_iterable(self):
        nc_range = NCRange(1)
        assert hasattr(nc_range, '__iter__')
        assert isinstance(iter(nc_range), Iterator)

    @mark.it("with single start value of 5, returns 0 to 4")
    def test_with_single_start_value(self):
        nc_range = NCRange(5)
        assert list(nc_range) == [0,1,2,3,4]

    @mark.it("returns the correct sequence for a given range")
    @mark.parametrize(
        'start,stop,step',
        [(1,5,1),(1,6,2),(5,1,-1),(5,1,1)],
        ids=[
            '(1,5,1) -> [1,2,3,4]',
            '(1,6,2) -> [1,3,5]',
            '(5,1,-1) -> [5,4,3,2]',
            '(5,1,1) -> []'
        ]
    )
    def test_gives_correct_range(self, start, stop, step):
        assert list(NCRange(start,stop,step)) == list(range(start,stop,step))

    def test_two_instances_with_same_values_are_equal(self):
        assert NCRange(1,5,1) == NCRange(1,5,1)

    def test_two_instances_with_different_values_are_not_equal(self):
        assert NCRange(1,5,1) != NCRange(1,5,2)

    def test_one_instance_is_not_equal_to_another_type(self):
        assert NCRange(1,5,1) != [1,5,1]

    @mark.it("returns the correct range object when sliced")
    def test_range_instance_is_sliceable(self):
        nc_range = NCRange(1,10,2)
        nc_range_sliced = nc_range[2:4]
        assert nc_range_sliced == NCRange(5,9,2)
        assert list(nc_range_sliced) == [5,7]
