// Initial heap implementation written in pure C
#include <stdio.h>

#define left_child(i) ((i << 1) + 1);
#define parent_of(i) ((i - 1) >> 1);
#define len(x) sizeof(x) / sizeof(x[0]);


void swap(int heap[], size_t x, size_t y) {
    int temp = heap[x];
    heap[x] = heap[y];
    heap[y] = temp;
}


void min_heapify(int heap[], size_t heap_size, size_t pos) {
    size_t parent = pos;
    pos = left_child(pos);

    while (pos < heap_size) {
        size_t right_pos = pos + 1;
        // if right-child has a value smaller than or equal to left-child
        if (right_pos < heap_size && heap[right_pos] <= heap[pos]) {
            // move pos to right-child
            pos = right_pos;
        }

        if (heap[pos] < heap[parent]) {
            swap(heap, pos, parent);
            parent = pos;
            pos = left_child(pos);
            continue;
        }
        break;
    }
}


int heap_replace(int heap[], size_t heap_size, int val) {
    // returns the smallest item in the list, replacing it with a given value
    int smallest = heap[0];
    heap[0] = val;
    min_heapify(heap, heap_size, 0);
    return smallest;
}


void heapify(int heap[], size_t heap_size) {
    // reorganises the a nodes so that they maintain the heap property
    size_t i = 1 + parent_of(heap_size);
    for (; i-- > 0;) {
        min_heapify(heap, heap_size, i);
    }
}

