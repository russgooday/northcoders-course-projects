import math
from typing import Union
from .internals import _NCRangeIterator

class NCRange:
    ''' A range object that can be sliced and iterated over.

    Arguments:
        *args (int): start, stop, step values for the range

    Returns:
        A new range object with the given start, stop and step values.
        If the range is sliced, a new range object is returned with the slice applied
        e.g. NCRange(1, 10, 1)[2:4] -> NCRange(3, 5, 1)
    '''
    def __init__(self, *args) -> None:

        if not args:
            raise ValueError('NCRange expected at least 1 argument, got 0')

        if not all(isinstance(arg, int) for arg in args):
            raise TypeError("'NoneType' object cannot be interpreted as an integer")

        # default starting values
        start, stop, step = 0,0,1

        if len(args) == 3:
            start, stop, step = args

            if step == 0:
                raise ValueError('arg 3 must not be zero')

        elif len(args) == 2:
            start, stop = args
        else:
            stop = args[0]

        self.start = start
        self.stop = stop
        self.step = step

    def __getitem(self, index: int) -> int:
        length = len(self)

        # for negative index add length
        if index < 0:
            index += length
        return self.start + index * self.step

    def __calc_slice(self, start: int, stop: int, step: int) -> tuple[int, ...]:
        """
        Calculates the slice applied to the range returning the new
        indexes and step.

        e.g.    NCRange(2,7,1)[0:3:2] -> (2, 5, 2)
                [2, 3, 4, 5, 6] -> [2, 4]
        Arguments:
            start (int): slice from index
            stop (int): slice up to index
            step (int): steps

        Returns:
            tuple[int,...]: start, stop and step indexes for new range
        """
        length = len(self)
        step = 1 if step is None else step

        if step == 0:
            raise ValueError('slice step must not be zero')

        is_reversed = step < 0

        if start is None:
            # either end of the range, depending on direction
            start = self.__getitem(-1 if is_reversed else 0)
        else:
            # convert negative start index to it's positive equivalent
            if start < 0:
                start += length
            start = self.__getitem(max(0, min(start, length)))

        if stop is None:
            # one step either side of the range, depending on direction
            stop = self.__getitem(-(length+1) if is_reversed else length)
        else:
            if stop < 0:
                stop += length
            stop = self.__getitem(max(-(length+1), min(stop, length-1 if is_reversed else length)))

        return start, stop, step * self.step

    def __index_within_bounds(self, index: int) -> bool:
        """checks if given index is within the range's indexes"""
        length = len(self)
        return -length <= index < length

    def __repr__(self) -> str:
        return f'NCRange({self.start}, {self.stop}, {self.step})'

    def __iter__(self):
        return _NCRangeIterator(self.start, self.step, len(self))

    def __eq__(self, other: 'NCRange') -> bool:
        if not isinstance(other, NCRange):
            return False
        return self.__dict__ == other.__dict__

    def __getitem__(self, index: Union[int, slice]) -> Union[int, '_NCRangeIterator']:

        if isinstance(index, int):
            if not self.__index_within_bounds(index):
                raise IndexError('range object index out of range')
            return self.__getitem(index)

        if isinstance(index, slice):
            # return a new range instance with the slice applied
            return NCRange(*self.__calc_slice(index.start, index.stop, index.step))

        raise TypeError('indices must be integers or a slice object')

    def __len__(self) -> int:
        start, stop, step = self.start, self.stop, self.step

        difference = stop - start if step > 0 else start - stop
        return 0 if difference < 0 else math.ceil(difference / abs(step))


if __name__ == '__main__':
    print(NCRange(1, 10, 1)[2:4]) # NCRange(3, 5, 1)
