from pytest import mark
from heapify.src.queue_time import queue_time

@mark.describe('various tests for queue_time')
class TestQueueTime():

    @mark.it('passed a an empty queue, it should return zero')
    def test_with_an_empty_queue(self):
        assert queue_time([]) == 0

    @mark.it("passed a queue with one customer, it should return that customer's time")
    def test_with_one_customer(self):
        assert queue_time([5]) == 5

    @mark.it(
        "passed a queue with numerous customers and one till it should return the sum of their times"
    )
    def test_with_numerous_customers_one_till(self):
        assert queue_time([5, 5], 1) == 10
        assert queue_time([3, 7, 5], 1) == 15

    @mark.it(
        """
        passed a queue with the same number of customers to tills
        it should return the maximum time in the queue
        """
    )
    def test_with_same_number_of_tills_to_customers(self):
        assert queue_time([5, 7], 2) == 7
        assert queue_time([9, 7, 5], 3) == 9

    @mark.it(
        "passed a queue with numerous customers and numerous tills it should equal the total queue time"
    )
    def test_with_numerous_customers_numerous_tills(self):
        assert queue_time([2, 3, 10], 2) == 12
        assert queue_time([2, 2, 2], 2) == 4
        assert queue_time([6, 2, 4, 5, 3, 2], 3) == 8
