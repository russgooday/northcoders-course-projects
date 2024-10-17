''' 
    time comparison between queue_time using a custom heap implementations and 
    queue_time_index_min using the built-in min and max functions.
'''
# pylint: disable=duplicate-code
import timeit
import random
from .queue_time import queue_time

def queue_time_index_min(queue: list, num_tills: int=2) -> int:
    ''' 
    Calculates the total queue time for a queue with a given number of tills 
    This version uses the built in min and max functions.
    '''
    if not queue:
        return 0

    if len(queue) < 2:
        return queue[0]

    if len(queue) == num_tills:
        return max(queue)

    if num_tills == 1:
        return sum(queue)

    tills = [0] * num_tills

    for t in queue:
        tills[tills.index(min(tills))] += t

    return max(tills)

if __name__ == '__main__':
    # create a random list
    rand_list = [random.randint(1, 100) for _ in range(1000)]
    print(queue_time(rand_list, 6))
    print(queue_time_index_min(rand_list, 6))

    def time_test_queue_time():
        ''' time the queue_time function '''
        queue = rand_list
        num_tills = 6
        return queue_time(queue, num_tills)

    def time_test_queue_time_index_min():
        ''' time the queue_time_index_min function '''
        queue = rand_list
        num_tills = 6
        return queue_time_index_min(queue, num_tills)

    print(timeit.timeit(time_test_queue_time_index_min, number=365))
    # Updated to use a custom heap implementation written in CPython
    print(timeit.timeit(time_test_queue_time, number=365))
