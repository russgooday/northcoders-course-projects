'''
    A limited clone of collections.Counter class.

    Purpose: Used as a learning exercise.
    -   To understand how the collections.Counter class works.

    -   To understand why subclassing a built in dict(written in C) has pitfalls such as
        shadowed methods being ignored

    -   To understand how to create a class that behaves like a dictionary without 
        subclassing dict and to understand how an ABC Mapping can be 
        subclassed to achieve this.

    -   To figure out how an instance of Countem can be updated with another instance 
        or dictionary.

    -   To grasp why recursion errors might occur, such as trying len(self), 
        iter(self) in dunder methods
'''
from typing import Dict, Iterable, List, Tuple, Any
from operator import itemgetter
from collections.abc import Mapping

__all__ = ['Countem']


def coalesce(*args: Any, check=None) -> Any:
    '''
        Args:
            *args: operands to test against check
            check: value to check inequality with
        Returns: first item to not equal check else None
    '''
    return next((x for x in args if x is not check), None)


def _count_elements(dictionary: Dict, iterable: Iterable) -> None:
    '''Update the dictionary with the counts of elements in the iterable'''
    for item in iterable:
        dictionary[item] = dictionary.get(item, 0) + 1

# Override with C helper function if available
try:
    from collections import _count_elements
except ImportError:
    pass

class Countem(Mapping):
    '''Creates a count of elements from an iterable

        Provides the more common dictionary methods as well as the following key methods:
        - max: Return the maximum count of any element in the dictionary
        - most_common: Return a list of the n most common elements in descending order
        - multi_mode: Returns the elements with the maximum count
        - update: Adds the counts of an other iterable to an instance of Countem in-place
        - subtract: Subtracts the counts of an other iterable from an instance of Countem in-place

        Args: iterable (Iterable): An iterable of elements to count
    '''
    def __init__(self, iterable: Iterable=None) -> None:
        self.__store = {}
        # if called Countem() will return an empty counter
        if iterable is not None:
            self.update(iterable)


    def update(self, iterable: Iterable) -> 'Countem':
        '''Add counted elements from an iterable to store'''

        if isinstance(iterable, Mapping):
            if self.__store:
                # optimize lookup for self.get
                self_get = self.get

                for k, v in iterable.items():
                    self[k] = v + self_get(k, 0)
            else:
                self.__store = dict(iterable)
        else:
            _count_elements(self, iterable)

        return self

    # Note: should results be limited to positives?
    def subtract(self, iterable: Iterable) -> 'Countem':
        '''Subtract counted elements from an iterable to store'''
        self_get = self.get

        if isinstance(iterable, Mapping):
            for k, v in iterable.items():
                self[k] = self_get(k, 0) - v
        else:
            for k in iterable:
                self[k] = self_get(k, 0) - 1

        return self


    def copy(self):
        '''Return a shallow copy of Countem instance'''
        return Countem(self.__store)


    def max(self) -> int|None:
        '''Return the maximum count of any element in the dictionary'''
        return max(self.values() or [None])


    def most_common(self, n: int = None) -> List[Tuple]:
        '''Return a list of the n most common elements in descending order'''
        return sorted(self.items(), reverse=True, key=itemgetter(1))[:coalesce(n, len(self))]


    def multi_mode(self) -> Tuple|None:
        '''Return the elements with the maximum count of any element in the dictionary'''
        maximum = self.max()
        return maximum and tuple(k for k,v in self.__store.items() if v == maximum)


    def __repr__(self) -> str:
        '''Return the string representation of the Countem instance in descending order'''
        return f'Countem({dict(self.most_common())!r})'


    def __len__(self) -> int:
        return len(self.__store)


    def __getitem__(self, key) -> Any:
        return self.__store[key]


    def __setitem__(self, key, value) -> None:
        self.__store[key] = value


    def __iter__(self) -> Iterable:
        return iter(self.__store)


    def __or__(self, other: 'Countem') -> 'Countem':
        '''union of counted elements from an iterable with store'''
        return self.copy().__ior__(other)


    def __ior__(self, other: 'Countem') -> 'Countem':
        '''in place union of counted elements from an iterable with store'''
        self_get = self.get

        for k, v in other.items():
            curr_v = self_get(k, 0)

            if v > curr_v:
                self[k] = v

        return self


    def __add__(self, other: Iterable) -> 'Countem':
        return self.copy().update(other)


    def __sub__(self, other: Iterable) -> 'Countem':
        return self.copy().subtract(other)
