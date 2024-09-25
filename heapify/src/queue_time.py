''' Calculate the total queue time for a queue with a given number of tills '''
# pylint: disable=consider-using-max-builtin
from . import heap_replace

def queue_time(queue: list, num_tills: int=2) -> int:
    ''' calculates the total queue time for a queue with a given number of tills '''
    if not queue:
        return 0

    if len(queue) < 2:
        return queue[0]

    if len(queue) == num_tills:
        return max(queue)

    if num_tills == 1:
        return sum(queue)

    tills = [0] * num_tills
    max_value = 0

    for t in queue:
        t += tills[0]
        if t > max_value:
            max_value = t
        heap_replace(tills, t)

    return max_value
