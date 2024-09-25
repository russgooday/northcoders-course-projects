''' Example usage of the Countem class. '''
from . import Countem, get_by_path

if __name__ == '__main__':
    c1 = Countem(['a', 'b', 'c'])
    c2 = Countem({'a': 1, 'b': 3, 'c': 3})

    print(c1)                       # Countem({'a': 1, 'b': 1, 'c': 1})
    c1 |= c2                        # Update c1 with c2
    print(c1)                       # Countem({'b': 3, 'c': 3, 'a': 1})
    print(c1.max())                 # 3
    print(c1.multi_mode())          # ('b', 'c')

    c3 = c1.copy()
    print(c3)                       # Countem({'b': 3, 'c': 3, 'a': 1})
    print(c3 == c1)                 # True
    c3.update('d')
    print(c3 == c1)                 # False
    print(c3)                       # Countem({'b': 3, 'c': 3, 'a': 1, 'd': 1})
    print(c3.most_common(3))        # [('b', 3), ('c', 3), ('a', 1)]
    print('d' in c3)                # True

    # Test CountemA + CountemB
    c4 = Countem('abc') + Countem('abcabc')
    print(c4)                       # Countem({'a': 3, 'b': 3, 'c': 3})

    # Test CountemA 'or' CountemB
    c5 = Countem('aaabc') | Countem('abbcc')
    print(c5)                       # Countem({'a': 3, 'b': 2, 'c': 2})

    # Test inplace CountemA 'ior' CountemB
    c6 = Countem('aaabc')
    c6 |= Countem('abbcc')
    print(c6)                       # Countem({'a': 3, 'b': 2, 'c': 2})

    students = [
        {'name': 'John', 'grades': {'math': 5, 'english': 3}},
        {'name': 'Jane', 'grades': {'math': 5, 'english': 4}},
        {'name': 'Sam', 'grades': {'math': 4, 'english': 4}},
        {'name': 'Joe', 'grades': {'math': 3, 'english': 5}},
        {'name': 'Jill', 'grades': {'math': 3, 'english': 3}},
        {'name': 'Jack', 'grades': {'math': 3, 'english': 3}},
        {'name': 'Paul', 'grades': {'math': 5, 'english': 5}}
    ]

    # Count the students' math grades
    math_grades_counter = Countem(map(get_by_path('grades','math'), students))
    print(math_grades_counter)              # Countem({5: 3, 3: 3, 4: 1})
    print('Most common math grade(s):', math_grades_counter.multi_mode())
    # Most common math grade(s): (5, 3)
