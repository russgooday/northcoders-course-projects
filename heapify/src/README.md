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

### Method:

<p class="codepen" data-height="300" data-default-tab="result" data-slug-hash="zYVQyyw" data-pen-title="heap visualisation" data-user="rpg2019" style="height: 300px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
  <span>See the Pen <a href="https://codepen.io/rpg2019/pen/zYVQyyw">
  heap visualisation</a> by Russell (<a href="https://codepen.io/rpg2019">@rpg2019</a>)
  on <a href="https://codepen.io">CodePen</a>.</span>
</p>
<script async src="https://cpwebassets.codepen.io/assets/embed/ei.js"></script>