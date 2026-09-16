# Two Sum — Complete Study, Interview, and Practice Guide

This README explains the **Two Sum** problem in depth using the optimized hash-map approach implemented in `two_sum_optimized.py`.

Your current implementation uses a one-pass dictionary:

```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen = {}

        for i, num in enumerate(nums):
            comp = target - num

            if comp in seen:
                return [seen[comp], i]

            seen[num] = i
```

The current hard-coded example is:

```python
nums = [2, 7, 11, 15]
target = 22
```

and it returns:

```python
[1, 3]
```

because:

```text
nums[1] + nums[3] = 7 + 15 = 22
```

---

## Table of Contents

1. Problem Statement
2. Why This Problem Matters
3. Core Mathematical Observation
4. Example Walkthrough
5. Solution Approaches
6. Why the One-Pass Hash Map Is Best
7. Pseudocode
8. Python Implementation Guidance
9. Test Cases
10. Complexity Analysis
11. Common Mistakes
12. Correctness Argument
13. Interview Questions
14. Similar LeetCode Problems
15. Non-LeetCode Exercises
16. Testing Strategies
17. Pattern Recognition
18. Further Extensions
19. Final Takeaways

---

# 1. Problem Statement

Given an integer array `nums` and an integer `target`, find the indices of **two distinct elements** whose values add up to `target`.

Formally, find `i` and `j` such that:

\[
nums[i] + nums[j] = target
\]

with:

\[
i \neq j
\]

Return the two indices:

```python
[i, j]
```

For the original LeetCode problem, the usual assumptions are:

- exactly one valid answer exists,
- the same array element cannot be used twice,
- the answer may be returned in any order.

### Example

Input:

```python
nums = [2, 7, 11, 15]
target = 9
```

Output:

```python
[0, 1]
```

because:

```text
2 + 7 = 9
```

---

# 2. Why This Problem Matters

Two Sum is one of the most important introductory interview problems because it teaches several reusable ideas:

- brute force vs optimized thinking,
- hash maps,
- complement search,
- time-space trade-offs,
- one-pass algorithms,
- constant-time average lookup,
- index tracking,
- duplicate handling,
- edge-case reasoning,
- recognizing when previously seen information should be stored.

The broad lesson is:

```text
Repeated searching is expensive.
If old information can help answer future questions quickly, store it.
```

---

# 3. Core Mathematical Observation

For the current number `x`, we need another value `y` such that:

\[
x + y = target
\]

Rearranging:

\[
y = target - x
\]

The value `y` is the **complement** of `x`.

In Python:

```python
comp = target - num
```

So rather than asking:

> Which pair of numbers adds to the target?

we can ask a simpler question while scanning:

> For the current number, what complement do I need, and have I already seen it?

---

# 4. Example Walkthrough

Consider:

```python
nums = [2, 7, 11, 15]
target = 22
```

Initially:

```python
seen = {}
```

The dictionary stores:

```text
number -> index
```

## Iteration 1

```text
i = 0
num = 2
```

Complement:

```text
22 - 2 = 20
```

Is `20` in `seen`?

```text
No
```

Store:

```python
seen[2] = 0
```

Now:

```python
seen = {2: 0}
```

## Iteration 2

```text
i = 1
num = 7
```

Complement:

```text
22 - 7 = 15
```

`15` has not been seen.

Store:

```python
seen[7] = 1
```

Now:

```python
seen = {
    2: 0,
    7: 1
}
```

## Iteration 3

```text
i = 2
num = 11
```

Complement:

```text
22 - 11 = 11
```

`11` is not yet in the dictionary, so we cannot use the current element twice.

Store:

```python
seen[11] = 2
```

## Iteration 4

```text
i = 3
num = 15
```

Complement:

```text
22 - 15 = 7
```

Now:

```python
7 in seen
```

is true.

The stored index is:

```python
seen[7] == 1
```

The current index is `3`.

Return:

```python
[1, 3]
```

---

# 5. Solution Approaches

## Approach 1 — Brute Force

Try every pair.

```python
def two_sum_bruteforce(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

### Complexity

Time:

\[
O(n^2)
\]

Space:

\[
O(1)
\]

### Why it is slow

For every element, we potentially compare it with many other elements.

For large arrays, the number of comparisons grows quadratically.

---

## Approach 2 — Two-Pass Hash Map

First record all values and indices:

```python
value_to_index = {}

for i, num in enumerate(nums):
    value_to_index[num] = i
```

Then search for complements:

```python
for i, num in enumerate(nums):
    comp = target - num

    if comp in value_to_index and value_to_index[comp] != i:
        return [i, value_to_index[comp]]
```

### Complexity

Average time:

\[
O(n)
\]

Space:

\[
O(n)
\]

This is good, but it requires two passes and an explicit check against reusing the same index.

---

## Approach 3 — One-Pass Hash Map

```python
def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        comp = target - num

        if comp in seen:
            return [seen[comp], i]

        seen[num] = i
```

### Complexity

Average time:

\[
O(n)
\]

Extra space:

\[
O(n)
\]

This is the preferred general solution.

---

# 6. Why the One-Pass Hash Map Is the Best General Solution

The standard Two Sum problem requires:

1. fast lookup,
2. preservation of original indices,
3. handling of duplicates,
4. avoidance of using the same element twice.

The one-pass dictionary solution satisfies all four naturally.

### Comparison

| Approach | Time | Extra Space | Preserves Original Indices Easily? |
|---|---:|---:|---|
| Brute force | `O(n²)` | `O(1)` | Yes |
| Two-pass hash map | `O(n)` avg. | `O(n)` | Yes |
| One-pass hash map | `O(n)` avg. | `O(n)` | Yes |
| Sorting + two pointers | `O(n log n)` | Depends | Requires extra handling |

The one-pass solution usually offers the best combination of simplicity and performance.

---

# 7. Why Check Before Inserting?

The order matters:

```python
if comp in seen:
    return [seen[comp], i]

seen[num] = i
```

Consider:

```python
nums = [3, 3]
target = 6
```

At index `0`:

```text
num = 3
comp = 3
```

The dictionary is empty, so no match exists yet.

Then:

```python
seen[3] = 0
```

At index `1`:

```text
num = 3
comp = 3
```

Now the first `3` is already stored.

Return:

```python
[0, 1]
```

This naturally enforces distinct indices.

---

# 8. Pseudocode

```text
FUNCTION TwoSum(nums, target):

    CREATE empty hash map seen

    FOR each index i and value num in nums:

        complement = target - num

        IF complement exists in seen:
            RETURN [stored index of complement, i]

        STORE:
            seen[num] = i
```

Compact mental version:

```text
for every number:
    needed = target - current_number

    if needed was seen before:
        return previous_index and current_index

    remember current_number
```

---

# 9. Python Implementation Guidance

## LeetCode-style version

LeetCode normally expects the method name `twoSum`:

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i
```

## Local hard-coded version

Your local structure can be:

```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen = {}

        for i, num in enumerate(nums):
            comp = target - num

            if comp in seen:
                return [seen[comp], i]

            seen[num] = i


nums = [2, 7, 11, 15]
target = 22

solution = Solution()
answer = solution.two_sum(nums, target)

print(answer)
```

Expected output:

```text
[1, 3]
```

---

# 10. Understanding `enumerate()`

This:

```python
for i, num in enumerate(nums):
```

gives both the index and value.

For:

```python
nums = [2, 7, 11]
```

you can think of `enumerate(nums)` as producing:

```text
(0, 2)
(1, 7)
(2, 11)
```

So:

```text
i   -> index
num -> value
```

Equivalent but more verbose code is:

```python
for i in range(len(nums)):
    num = nums[i]
```

---

# 11. Understanding the Dictionary

The line:

```python
seen[num] = i
```

stores:

```text
value -> index
```

Example:

```python
seen = {
    2: 0,
    7: 1,
    11: 2
}
```

Then:

```python
seen[7]
```

returns:

```python
1
```

A dictionary is preferable to a set here because the problem asks for indices, not only existence.

---

# 12. Multiple Test Cases

## Test Case 1 — Standard

```python
nums = [2, 7, 11, 15]
target = 9
```

Expected:

```python
[0, 1]
```

---

## Test Case 2 — Current Hard-Coded Example

```python
nums = [2, 7, 11, 15]
target = 22
```

Expected:

```python
[1, 3]
```

---

## Test Case 3 — Pair Later in Array

```python
nums = [3, 2, 4]
target = 6
```

Expected:

```python
[1, 2]
```

---

## Test Case 4 — Duplicate Values

```python
nums = [3, 3]
target = 6
```

Expected:

```python
[0, 1]
```

---

## Test Case 5 — Negative Numbers

```python
nums = [-3, 4, 3, 90]
target = 0
```

Expected:

```python
[0, 2]
```

---

## Test Case 6 — Zero

```python
nums = [0, 4, 3, 0]
target = 0
```

Expected:

```python
[0, 3]
```

---

## Test Case 7 — Negative Target

```python
nums = [-5, -2, -8, 4]
target = -10
```

Expected:

```python
[1, 2]
```

---

## Test Case 8 — Large Magnitudes

```python
nums = [1000000, -999999, 7, 12]
target = 1
```

Expected:

```python
[0, 1]
```

---

# 13. Running Multiple Test Cases Automatically

```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen = {}

        for i, num in enumerate(nums):
            comp = target - num

            if comp in seen:
                return [seen[comp], i]

            seen[num] = i


solution = Solution()

test_cases = [
    ([2, 7, 11, 15], 9),
    ([2, 7, 11, 15], 22),
    ([3, 2, 4], 6),
    ([3, 3], 6),
    ([-3, 4, 3, 90], 0),
    ([0, 4, 3, 0], 0),
]

for nums, target in test_cases:
    result = solution.two_sum(nums, target)
    print(f"nums={nums}, target={target}, result={result}")
```

---

# 14. Complexity Analysis

## Brute Force

Nested loops:

```python
for i in range(n):
    for j in range(i + 1, n):
```

lead to roughly:

\[
\frac{n(n-1)}{2}
\]

pair checks.

Therefore:

\[
O(n^2)
\]

---

## Hash Map

The array is scanned once.

Each average dictionary lookup is:

\[
O(1)
\]

Each average insertion is:

\[
O(1)
\]

Therefore:

\[
n \times O(1) = O(n)
\]

Extra dictionary storage may contain up to `n` values:

\[
O(n)
\]

So:

```text
Average Time Complexity: O(n)
Space Complexity:        O(n)
```

---

# 15. Time-Space Trade-Off

Brute force saves memory but uses more time:

```text
Time  = O(n²)
Space = O(1)
```

The dictionary solution uses extra memory to reduce runtime:

```text
Time  = O(n)
Space = O(n)
```

This is a classic interview example of a **time-space trade-off**.

---

# 16. Common Mistakes

## Mistake 1 — Returning Values Instead of Indices

Wrong:

```python
return [comp, num]
```

Correct:

```python
return [seen[comp], i]
```

---

## Mistake 2 — Using the Same Element Twice

For:

```python
nums = [3, 2, 4]
target = 6
```

you cannot use the `3` at index `0` twice.

---

## Mistake 3 — Repeatedly Using `.index()`

This looks tempting:

```python
if target - num in nums:
    return [i, nums.index(target - num)]
```

Problems:

- membership lookup in a list is `O(n)`,
- `.index()` is also `O(n)`,
- duplicates can cause incorrect indices,
- total complexity may become `O(n²)`.

---

## Mistake 4 — Sorting Without Preserving Indices

Sorting changes positions.

Example:

```python
nums = [10, 2, 7]
```

becomes:

```python
[2, 7, 10]
```

If the problem asks for original indices, additional index bookkeeping is required.

---

## Mistake 5 — Ignoring Duplicates

This case must work:

```python
nums = [3, 3]
target = 6
```

---

## Mistake 6 — Forgetting the No-Solution Case Outside LeetCode

The original problem guarantees a solution.

General-purpose code may instead need:

```python
return None
```

or:

```python
return []
```

---

# 17. More Robust Local Version

```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int] | None:
        seen = {}

        for i, num in enumerate(nums):
            comp = target - num

            if comp in seen:
                return [seen[comp], i]

            seen[num] = i

        return None
```

Example:

```python
nums = [1, 2, 3]
target = 100
```

returns:

```python
None
```

---

# 18. Formal Correctness Argument

Suppose a valid solution exists at indices `j` and `i` with:

\[
j < i
\]

and:

\[
nums[j] + nums[i] = target
\]

When index `j` is processed, the algorithm stores:

```python
seen[nums[j]] = j
```

When index `i` is processed:

\[
comp = target - nums[i]
\]

Since:

\[
nums[j] + nums[i] = target
\]

we have:

\[
target - nums[i] = nums[j]
\]

Therefore:

```python
comp in seen
```

is true.

The algorithm returns:

```python
[j, i]
```

Thus, whenever a valid pair exists, the one-pass algorithm will discover it when the later index is processed.

---

# 19. Interview Explanation Template

A concise answer suitable for an interview:

> A brute-force solution checks every pair and takes O(n²) time. I can reduce this to O(n) expected time using a hash map. While traversing the array, I compute the complement `target - nums[i]`. If that complement has already been seen, I return its stored index together with the current index. Otherwise, I store the current number and its index. The algorithm uses O(n) additional space.

---

# 20. Easy Interview Questions

### Q1. What is the brute-force approach?

Check every possible pair.

Complexity:

```text
Time:  O(n²)
Space: O(1)
```

### Q2. What is a complement?

For current value `x`:

\[
complement = target-x
\]

### Q3. What does `seen` store?

```text
value -> index
```

### Q4. Why use `enumerate()`?

Because the algorithm needs both the value and its index.

### Q5. Why use a dictionary instead of a list search?

Dictionary membership is average `O(1)` instead of list membership `O(n)`.

### Q6. Does the solution support negative numbers?

Yes.

### Q7. Does it support duplicates?

Yes.

### Q8. Why not return `[num, comp]`?

Because the problem asks for indices.

---

# 21. Medium Interview Questions

### Q1. Why check the complement before inserting the current number?

To prevent the current array position from satisfying the pair with itself.

### Q2. What happens if multiple answers exist?

This implementation returns the first valid pair encountered during left-to-right traversal.

### Q3. How would you return all valid index pairs?

Continue scanning instead of returning immediately, and store enough index history to handle repeated values.

### Q4. Can Two Sum be solved with sorting?

Yes. Sort while preserving original indices and then use two pointers.

### Q5. What is the complexity of sorting + two pointers?

```text
Sorting: O(n log n)
Scan:    O(n)

Overall: O(n log n)
```

### Q6. What changes if there may be no solution?

Return `None`, `[]`, or raise a suitable exception depending on the API design.

### Q7. Why is hash-table lookup described as average O(1) rather than guaranteed O(1)?

Hash collisions and implementation details can create worse-case behavior, though Python dictionaries are designed for efficient average access.

### Q8. When would a set be enough?

When you only need to know whether a complement exists and do not need its index.

---

# 22. Difficult Interview Questions

### Q1. Solve Two Sum without O(n) extra memory.

A common approach is:

```text
sort + two pointers
```

The challenge is preserving original indices.

### Q2. How would you process an infinite stream?

Maintain the same `seen` structure. For every incoming number, check its complement against earlier values.

### Q3. How would you count all index pairs?

Use a frequency map.

Example pattern:

```python
count = 0
freq = {}

for num in nums:
    count += freq.get(target - num, 0)
    freq[num] = freq.get(num, 0) + 1
```

### Q4. How would you solve 3Sum?

Typical strategy:

```text
sort
fix one element
solve Two Sum with two pointers for the remainder
```

Typical time:

\[
O(n^2)
\]

### Q5. How would you generalize to k-Sum?

Typical strategy:

```text
sorting + recursion
```

Reduce `k-Sum` to `(k-1)-Sum` until reaching a Two Sum base case.

### Q6. What if the array is too large for memory?

Discuss:

- external sorting,
- database indexes,
- streaming,
- partitioning,
- distributed hash structures,
- chunk-based processing.

### Q7. Can the one-pass solution be parallelized trivially?

Not completely. The method depends on previously seen values. Parallel designs normally require partitioning, synchronization, or a different formulation.

### Q8. If memory is more expensive than CPU time, which approach might you prefer?

Depending on constraints, brute force or sorting/two-pointers may be preferable because they can reduce auxiliary memory.

---

# 23. Similar LeetCode Problems

These problems build on related patterns.

| Problem | Number | Main Pattern |
|---|---:|---|
| Two Sum | 1 | Hash map |
| 3Sum | 15 | Sorting + two pointers |
| 3Sum Closest | 16 | Two pointers |
| 4Sum | 18 | k-Sum / two pointers |
| Contains Duplicate | 217 | Hash set |
| Contains Duplicate II | 219 | Hash map / sliding window |
| Intersection of Two Arrays | 349 | Hash set |
| 4Sum II | 454 | Pair sums + hash map |
| Subarray Sum Equals K | 560 | Prefix sum + hash map |
| Two Sum IV — Input Is a BST | 653 | Tree + set / two pointers |
| Longest Consecutive Sequence | 128 | Hash set |
| Two Sum II — Input Array Is Sorted | 167 | Two pointers |

A useful practice order:

```text
1.  LeetCode 1   — Two Sum
2.  LeetCode 217 — Contains Duplicate
3.  LeetCode 349 — Intersection of Two Arrays
4.  LeetCode 219 — Contains Duplicate II
5.  LeetCode 167 — Two Sum II
6.  LeetCode 15  — 3Sum
7.  LeetCode 560 — Subarray Sum Equals K
8.  LeetCode 454 — 4Sum II
9.  LeetCode 128 — Longest Consecutive Sequence
10. LeetCode 18  — 4Sum
```

---

# 24. Non-LeetCode Exercise 1 — Pair With Given Difference

## Problem

Given an array and integer `k`, determine whether two distinct values exist such that:

\[
|a-b|=k
\]

Example:

```python
nums = [5, 20, 3, 2, 50, 80]
k = 78
```

Expected:

```text
True
```

because:

```text
80 - 2 = 78
```

### Test Cases

```python
([5, 20, 3, 2, 50, 80], 78) -> True
([1, 2, 3, 4], 10)           -> False
([8, 8], 0)                   -> True
([-5, -1, 3], 4)              -> True
```

---

# 25. Non-LeetCode Exercise 2 — Count Pairs With Target Sum

## Problem

Count index pairs satisfying:

\[
nums[i]+nums[j]=target
\]

where:

\[
i<j
\]

Example:

```python
nums = [1, 5, 7, -1, 5]
target = 6
```

Expected:

```text
3
```

### Test Cases

```python
([1, 5, 7, -1, 5], 6) -> 3
([1, 1, 1, 1], 2)      -> 6
([2, 4, 6], 20)        -> 0
([-3, 3, 0], 0)         -> 1
```

---

# 26. Non-LeetCode Exercise 3 — Pair Product

## Problem

Find two distinct elements whose product equals `target`.

\[
a \times b = target
\]

Example:

```python
nums = [2, 3, 4, 6]
target = 12
```

Valid answers include:

```text
2 × 6 = 12
3 × 4 = 12
```

### Test Cases

```python
([2, 3, 4, 6], 12) -> valid pair exists
([1, 5, 10], 50)    -> indices [1, 2]
([0, 2, 5], 0)      -> valid pair involving index 0
([-2, 4, -3], 6)    -> indices [0, 2]
```

Watch for division by zero if trying to derive a multiplicative complement.

---

# 27. Non-LeetCode Exercise 4 — Closest Pair Sum

## Problem

Find two numbers whose sum is closest to a target.

Example:

```python
nums = [10, 22, 28, 29, 30, 40]
target = 54
```

A best pair is:

```text
22 + 30 = 52
```

Difference:

```text
|54 - 52| = 2
```

### Test Cases

```python
([10, 22, 28, 29, 30, 40], 54)
([1, 4, 7, 10], 15)
([-10, -3, 1, 8], 0)
```

Hint:

```text
Sort + two pointers
```

---

# 28. Non-LeetCode Exercise 5 — Return All Unique Pairs

## Problem

Return all unique value pairs whose sum equals `target`.

Example:

```python
nums = [1, 2, 3, 2, 4, 3]
target = 5
```

Expected:

```python
[(1, 4), (2, 3)]
```

### Test Cases

```python
([1, 2, 3, 2, 4, 3], 5)
([1, 1, 1, 1], 2)
([-2, -1, 0, 1, 2], 0)
([5, 5, 5], 10)
```

---

# 29. Non-LeetCode Exercise 6 — Two Sum Data Structure

Design:

```python
class TwoSum:
    def add(self, number):
        ...

    def find(self, target):
        ...
```

Example:

```python
obj = TwoSum()

obj.add(1)
obj.add(3)
obj.add(5)

obj.find(4)  # True
obj.find(7)  # False
```

Interview follow-up:

> Would you optimize `add()` or `find()`?

There is no single correct answer; it depends on which operation is called more frequently.

---

# 30. Non-LeetCode Exercise 7 — Pair Sum Across Two Arrays

## Problem

Given arrays `a` and `b`, find one element from each such that:

\[
a[i]+b[j]=target
\]

Example:

```python
a = [1, 4, 8]
b = [2, 5, 10]
target = 9
```

Expected valid pair:

```text
4 + 5 = 9
```

### Test Cases

```python
([1, 4, 8], [2, 5, 10], 9) -> True
([3, 7], [4, 8], 20)        -> False
([-2, 5], [3, 8], 1)        -> True
```

---

# 31. Non-LeetCode Exercise 8 — First Pair Seen in a Stream

## Problem

Numbers arrive one at a time. Return the first pair of positions whose values sum to a fixed target.

Example stream:

```text
8, 5, 1, 9, 4
```

Target:

```text
13
```

The first valid pair encountered is:

```text
8 + 5 = 13
```

Think about why the one-pass dictionary design is already naturally suited to this problem.

---

# 32. Manual Dry-Run Exercises

Do these without executing code.

## Exercise A

```python
nums = [8, 3, 12, 5, 7]
target = 10
```

Expected:

```python
[1, 4]
```

## Exercise B

```python
nums = [10, -2, 7, 5]
target = 3
```

Expected:

```python
[1, 3]
```

## Exercise C

```python
nums = [6, 1, 4, 9, 3]
target = 10
```

One valid result:

```python
[1, 3]
```

## Exercise D

```python
nums = [5, 5, 5, 5]
target = 10
```

Determine exactly which pair the one-pass implementation returns first.

---

# 33. Testing With Assertions

```python
solution = Solution()

assert solution.two_sum([2, 7, 11, 15], 9) == [0, 1]
assert solution.two_sum([3, 2, 4], 6) == [1, 2]
assert solution.two_sum([3, 3], 6) == [0, 1]

print("All tests passed.")
```

Assertions are useful because Python immediately reports a failure if an expected result is wrong.

---

# 34. Unit Testing With `unittest`

```python
import unittest


class Solution:
    def two_sum(self, nums, target):
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return None


class TestTwoSum(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_standard(self):
        self.assertEqual(
            self.solution.two_sum([2, 7, 11, 15], 9),
            [0, 1]
        )

    def test_duplicates(self):
        self.assertEqual(
            self.solution.two_sum([3, 3], 6),
            [0, 1]
        )

    def test_negative(self):
        self.assertEqual(
            self.solution.two_sum([-3, 4, 3, 90], 0),
            [0, 2]
        )

    def test_no_solution(self):
        self.assertIsNone(
            self.solution.two_sum([1, 2, 3], 100)
        )


if __name__ == "__main__":
    unittest.main()
```

---

# 35. Production-Style Function With a Docstring

```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int] | None:
        """
        Return indices of two distinct elements whose sum equals target.

        Parameters
        ----------
        nums : list[int]
            Input list of integers.

        target : int
            Desired sum.

        Returns
        -------
        list[int] | None
            Two indices whose values sum to target.
            Returns None when no pair exists.

        Complexity
        ----------
        Average time: O(n)
        Extra space: O(n)
        """

        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return None
```

---

# 36. Hash Set vs Hash Map

A set stores only values:

```python
seen = {2, 7, 11}
```

It answers:

```text
Have I seen this value?
```

A dictionary stores key-value pairs:

```python
seen = {
    2: 0,
    7: 1,
    11: 2
}
```

It answers both:

```text
Have I seen this value?
```

and:

```text
At what index did I see it?
```

Since Two Sum requires indices, a dictionary is the natural structure.

---

# 37. Pattern Recognition

When you encounter a new interview problem, ask:

### Question 1

Do I repeatedly need to determine whether some value has already appeared?

If yes, think:

```text
hash set / hash map
```

### Question 2

Can I derive the exact value I need?

For Two Sum:

\[
needed = target-current
\]

### Question 3

Do I need associated information such as an index, count, or position?

If yes, prefer a dictionary over a set.

Examples:

```text
value -> index
value -> frequency
prefix_sum -> count
character -> last_seen_position
```

---

# 38. The Generic Hash-Map Template

A useful generic structure is:

```python
seen = {}

for i, x in enumerate(data):

    needed = derive_needed_value(x)

    if needed in seen:
        return ...

    seen[x] = i
```

The important part is not memorizing the exact syntax.

The important part is recognizing:

```text
current information
        ↓
derive what is needed
        ↓
check previously stored information
```

---

# 39. Further Extensions

Once Two Sum feels easy, try implementing:

1. return values instead of indices,
2. return all index pairs,
3. return all unique value pairs,
4. count all valid pairs,
5. sorted Two Sum with two pointers,
6. closest pair sum,
7. pair with a fixed difference,
8. pair with fixed product,
9. Two Sum in a binary search tree,
10. Two Sum in a stream,
11. Three Sum,
12. Four Sum,
13. general k-Sum,
14. subarray sum equals target,
15. pair sums across two arrays.

---

# 40. What You Should Be Able to Explain After Studying This

You should be able to answer:

- Why is brute force `O(n²)`?
- Why is the hash-map solution average `O(n)`?
- Why do we need a dictionary rather than only a set?
- What exactly is stored in `seen`?
- What is the complement?
- Why is the complement checked before inserting the current value?
- Why does `[3, 3]` work correctly?
- Why is repeated `nums.index()` inefficient?
- What is the time-space trade-off?
- How could you solve the problem using sorting?
- When would two pointers be preferable?
- How would you generalize from Two Sum to Three Sum?
- How would the algorithm change if no solution were guaranteed?
- How would you count all pairs instead of finding one?

If you can explain these clearly without referring to the code, you understand the problem rather than merely memorizing the implementation.

---

# 41. Final Takeaways

The central mathematical relation is:

\[
complement = target-current
\]

The central data-structure idea is:

```text
value -> index
```

The central optimization is:

```text
Instead of repeatedly searching the array,
remember values already encountered.
```

Brute force:

```text
Time:  O(n²)
Space: O(1)
```

Preferred one-pass hash map:

```text
Average Time: O(n)
Extra Space:  O(n)
```

The mental model to retain is:

```text
For the current value:
    What partner do I need?

Have I already seen that partner?
    Yes -> return the pair
    No  -> remember the current value
```

That reasoning pattern is far more valuable than memorizing the six lines of code.
