'''
currently a work in progress adjusted for zero indexed arrays:
'''

def left_child(i:int) -> int:
    ''' returns the index of the left child of the node '''
    return (i << 1) + 1

def right_child(i:int) -> int:
    ''' returns the index of the right child of the node '''
    return (i << 1) + 2

def get_parent(i:int) -> int:
    ''' returns the index of the node's parent '''
    return i - 1 >> 1


def min_heapify(heap: list, pos:int) -> None:
    ''' reorganises the a nodes from a given index so that they maintain the heap property '''
    heap_size = len(heap)
    parent = pos
    # move pos to left-child
    pos = left_child(pos)

    while pos < heap_size:
        right_pos = pos + 1

        # if right-child has a value smaller than or equal to left-child
        if right_pos < heap_size and heap[right_pos] <= heap[pos]:
            # move pos to right-child
            pos = right_pos

        if heap[pos] < heap[parent]:
            heap[pos], heap[parent] = heap[parent], heap[pos]
            parent = pos
            pos = left_child(pos)
            continue
        break


def heapify(lst: list) -> list:
    ''' reorganises the a nodes so that they maintain the heap property '''
    for i in range(get_parent(len(lst)), -1, -1):
        min_heapify(lst, i)
    return lst


def heap_replace(lst: list, val: int) -> int:
    ''' returns the smallest item in the list, replacing it with a given value '''
    smallest = lst[0]
    lst[0] = val
    min_heapify(lst, 0)
    return smallest
