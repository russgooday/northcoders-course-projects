# Supermarket Queue
You are a middle manager in a large supermarket chain, tasked with overseeing the checkout queue.

Every once in a while, your boss radios you to ask how long the current queues will take to process. You take this job seriously, so you've decided to write a function called queue_time to solve the problem.

The function takes two arguments:

- **customers**: a list of positive integers representing the queue. Each integer represents a customer, and its value is the amount of time they require to check out.
- **checkouts**: a positive integer, the number of checkout tills.

The function should return the time required to process all the customers.

- There is only ONE queue.
- The order of the queue NEVER changes.
- Assume that the front person in the queue (i.e. the first element in the list) proceeds to a till as soon as it becomes free.
## Examples:
```
queue_time([2, 2, 2], 1)
# returns 6 because just one checkout means the total time is just the sum of the times

queue_time([2, 10], 2)
# returns 10 because each customer has immediate access to a checkout and the slowest customer is 10

queue_time([2, 2, 2], 2)
# returns 4 because the first 2 customers have immediate access to a checkout, and then one customer is left to be processed

queue_time([2, 3, 10], 2)
# returns 12, because the first checkout will deal with the 2 minute customer, and then the 10 minute customer - totalling 12 minutes
```

## How I approached this exercise

### Solution:

To calculate the time required to process all customers, we can use a simple approach. Each checkout till will maintain a running total of the time taken to serve its customers. The next customer in the queue will always go to the till with the current lowest total time.

Once all customers have been served, the total time required will be held in the till with the maximum value.

**A simple example with 2 tills and 6 customers.**

<img alt='example of priority queue' width='600px' src='images/queue_example.gif'/>

### The code:

With a loop the built in `min` and `max` methods can be used to achieve this.

```python
# create a list of tills with initial times set to zero
tills = [0] * num_tills

for t in queue:
    # find the index of the till with the lowest time
    # and add to that the time of the current customer(t)
    tills[tills.index(min(tills))] += t

# return the till with the maximum value
return max(tills)
```

### An alternative approach using a heap queue

An alternative to using the built in `min` method is to use Python's [heapq](https://docs.python.org/3/library/heapq.html) module. This module uses a binary tree based heap data structure or priority queue. On popping and replacing the root item (heap replace) a partial descending sort is carried out on the tree, where smaller children nodes are swapped with their parent. This results in the smallest value being stored in the root node.

The interesting aspect to this data structure is that the tree is stored in a fixed sized array, with the nodes stored in indexes. The indexes of the parent and children are navigated through with some simple calculations.

```
left_child = i * 2 + 1
right_child = i * 2 + 2
parent = (i - 1) / 2
```

<img alt='heap visualisation' width='600px' src='images/heap-visualisation.gif'/>

The following example is of heap replace on the previous heapified list. The function extracts the root value and replace it with a new value. The function then does a partial sort to maintain `min-heap`.

<img alt='example of heap replace' width='600px' src='images/heap-replace.gif'/>

### Custom heap modules

To better understand how the algorithm works, I created my own heap functions and modules. My initial function was written in python.

[internals/_heapify.py](internals/_heapify.py)

This function offered very little performance improvements if any over the built in `min` and `max` functions.

### C and CPython modules

I was keen to see what gains a C implementation would achieve. I haven't programmed in C before, so this was very much unchartered territory.

The pure C version was relatively simple to implement
[internals/lib/heapify.c](internals/lib/heapify.c)

The CPython version was a whole different story. I had to refer a great deal to heapq's source code. Getting to grips with PyObjects, error handling, pointers, the need to deal with refs and general setup was a real challenge. It is something I want to spend more time on to get a better understanding.

[internals/lib/heapify.c](internals/lib/_heapify.c)

### The queue time code:

Very similar to the min and max implementation.
```python
tills = [0] * num_tills
max_value = 0

for t in queue:
    t += tills[0]
    if t > max_value:
        max_value = t
    heap_replace(tills, t)

return max_value
```

In the brief tests I did, the CPython module was 3x faster than the built-in `min` and `max`.

### Conclusion

The project could have been signed off with the Python built-ins or the heapq module. I used this project as a learning exercise, to improve my programming skills and getter a broader knowledge of algorithms. Altogether, a very enjoyable and rewarding exercise.
