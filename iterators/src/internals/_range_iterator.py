''' Internal Range Iterator for Range class '''

class _NCRangeIterator:
    """ Range Iterator
        Arguments:
            start (int): start value
            step (int): step value
            length (int): number of elements in the range
    """

    def __init__(self, start: int, step: int, length: int) -> None:
        self.start = start
        self.step = step
        self.length = length
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.length:
            raise StopIteration

        value = self.start + self.index * self.step
        self.index += 1
        return value
