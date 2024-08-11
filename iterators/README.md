# Iterables and Iterators
## Range

### Task
You will be implementing your own version of this object (NCRange), as far as possible following the specification in the documentation.

However you will probably find it difficult to make your range object subscriptable or sliceable (e.g. defining r[:2] or r[4]) so this functionality is optional.

### Result
Making the range object sliceable was indeed a challenge. The built-in range function, when sliced returns a new range object with tranformed start, stop and step values.

This means we have to calculate for numerous combinations of ascending or descending ranges, slices and steps.

Slices also work on indexes, and these can include negative indexes.
For example with the following range `range(1, 10, 3)[:-1]`, which contains the numbers `1, 4, 7` the new range would be `range(1, 7, 3)`. The last index is ignored so this new range contains only `1, 4`.

There was a great deal of testing with trial and error involved. I worked through a multitude of tests comparing my results with Python's inbuilt range. This included dealing with nonsensical ranges or slices like (1, 10, -2).

The range class I have built does have validation/error handling and I have tried to follow the built in behaviour in this regard.

As an aside this exercise lead me to writing an equivalent range class in Javascript — a language without built in range functionality. The link if you are interested is [here](https://github.com/russgooday/JS-Snippets/blob/main/range/src/range.js)






