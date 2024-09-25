''' Examples of the find_most_repeated function utilising the Countem class '''

from .find_most_repeated import find_most_repeated

if __name__ == '__main__':
    # Examples
    print(find_most_repeated([]))
    # {'elements': [], 'repeats': None}

    print(find_most_repeated(['a','b','c']))
    # {'elements': [], 'repeats': None}

    print(find_most_repeated(['a','b','b','c']))
    # {'elements': ['b'], 'repeats': 2}

    print(find_most_repeated(['a', 'b', 'b', 3, 'c', 3, 'c', 3, 'b']))
    # {'elements': ['b', 3], 'repeats': 3}
