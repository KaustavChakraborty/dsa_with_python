# LeetCode 3 — Longest Substring Without Repeating Characters

> **Topic:** Strings, Hashing, Two Pointers, Sliding Window  
> **Difficulty:** Medium  
> **Primary interview pattern:** Variable-size sliding window  
> **Target complexity:** `O(n)` time  
> **Language used here:** Python  
> **Core implementation:** Set-based sliding window  
> **Also covered:** Last-seen-index dictionary optimization, correctness proof, interview Q&A, related problems, exercises

---

# Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [What This Problem Is Really Testing](#2-what-this-problem-is-really-testing)
3. [Substring vs Subsequence](#3-substring-vs-subsequence)
4. [Examples and Test Cases](#4-examples-and-test-cases)
5. [Start With the Brute-Force Idea](#5-start-with-the-brute-force-idea)
6. [Why Brute Force Is Not Good Enough](#6-why-brute-force-is-not-good-enough)
7. [The Sliding-Window Insight](#7-the-sliding-window-insight)
8. [The Window Invariant](#8-the-window-invariant)
9. [Set-Based Sliding-Window Solution](#9-set-based-sliding-window-solution)
10. [Line-by-Line Explanation](#10-line-by-line-explanation)
11. [Why `while`, Not `if`?](#11-why-while-not-if)
12. [Detailed Dry Run: `abcabcbb`](#12-detailed-dry-run-abcabcbb)
13. [Detailed Dry Run: `abba`](#13-detailed-dry-run-abba)
14. [Detailed Dry Run: `pwwkew`](#14-detailed-dry-run-pwwkew)
15. [Detailed Dry Run: `dvdf`](#15-detailed-dry-run-dvdf)
16. [Correctness Argument](#16-correctness-argument)
17. [Complexity Analysis](#17-complexity-analysis)
18. [Why the Nested `while` Loop Is Still O(n)](#18-why-the-nested-while-loop-is-still-on)
19. [Dictionary / Last-Seen Optimization](#19-dictionary--last-seen-optimization)
20. [Why `max(left, last_seen[c] + 1)` Matters](#20-why-maxleft-last_seenc--1-matters)
21. [Set vs Dictionary Solution](#21-set-vs-dictionary-solution)
22. [Python Implementation Guidance](#22-python-implementation-guidance)
23. [Common Mistakes](#23-common-mistakes)
24. [Edge Cases](#24-edge-cases)
25. [How to Explain This in an Interview](#25-how-to-explain-this-in-an-interview)
26. [How to Recognize Sliding-Window Problems](#26-how-to-recognize-sliding-window-problems)
27. [Generic Sliding-Window Templates](#27-generic-sliding-window-templates)
28. [Interview Questions — Easy](#28-interview-questions--easy)
29. [Interview Questions — Medium](#29-interview-questions--medium)
30. [Interview Questions — Difficult](#30-interview-questions--difficult)
31. [Follow-Up Variations an Interviewer May Ask](#31-follow-up-variations-an-interviewer-may-ask)
32. [Similar LeetCode Problems](#32-similar-leetcode-problems)
33. [Non-LeetCode Practice Problems](#33-non-leetcode-practice-problems)
34. [Test Strategy](#34-test-strategy)
35. [Debugging Checklist](#35-debugging-checklist)
36. [Pattern Recognition Cheat Sheet](#36-pattern-recognition-cheat-sheet)
37. [Practice Roadmap](#37-practice-roadmap)
38. [Final Takeaways](#38-final-takeaways)

---

# 1. Problem Statement

Given a string `s`, return the **length of the longest substring without repeating characters**.

A **substring** is a contiguous sequence of characters inside a string.

## Example 1

```text
Input:
s = "abcabcbb"

Output:
3
```

Explanation:

Possible longest substrings include:

```text
"abc"
"bca"
"cab"
```

All have length `3`.

---

## Example 2

```text
Input:
s = "bbbbb"

Output:
1
```

The longest substring without repeated characters is:

```text
"b"
```

---

## Example 3

```text
Input:
s = "pwwkew"

Output:
3
```

Valid answers include:

```text
"wke"
"kew"
```

The answer is therefore:

```text
3
```

Note that `"pwke"` is **not** a substring because its characters are not contiguous.

---

# 2. What This Problem Is Really Testing

This problem is not mainly about strings.

It tests whether you can recognize and correctly implement the following ideas:

- variable-size sliding window
- two-pointer reasoning
- maintaining a window invariant
- hash-set membership
- incremental state updates
- avoiding redundant recomputation
- amortized complexity analysis
- careful duplicate handling
- distinguishing substring from subsequence
- maintaining the best answer while scanning

The key pattern is:

```text
EXPAND RIGHT
     |
     v
Does the window violate the condition?
     |
    YES
     |
     v
SHRINK LEFT
     |
     v
Window valid again
     |
     v
UPDATE ANSWER
```

For LeetCode 3, the condition is:

> Every character inside the current window must be unique.

---

# 3. Substring vs Subsequence

This distinction is fundamental.

Consider:

```text
s = "pwwkew"
```

A substring must use consecutive positions.

Examples of substrings:

```text
"p"
"pw"
"pww"
"wwk"
"wke"
"kew"
```

But:

```text
"pwke"
```

is not a substring, because characters were skipped.

A subsequence allows skipping characters.

For example:

```text
p w w k e w
^   ^ ^ ^
p   w k e
```

So `"pwke"` can be a subsequence, but it is not a substring.

Because LeetCode 3 requires a substring, we need to reason about a **contiguous interval**:

```text
[left, right]
```

This is exactly why the two-pointer / sliding-window approach is natural.

---

# 4. Examples and Test Cases

You should be comfortable predicting all of these before coding.

| Input | Expected Output | One Longest Valid Substring |
|---|---:|---|
| `""` | `0` | `""` |
| `"a"` | `1` | `"a"` |
| `"aaaaa"` | `1` | `"a"` |
| `"abc"` | `3` | `"abc"` |
| `"abcabcbb"` | `3` | `"abc"` |
| `"bbbbb"` | `1` | `"b"` |
| `"pwwkew"` | `3` | `"wke"` |
| `"abba"` | `2` | `"ab"` or `"ba"` |
| `"dvdf"` | `3` | `"vdf"` |
| `"tmmzuxt"` | `5` | `"mzuxt"` |
| `"anviaj"` | `5` | `"nviaj"` |
| `"aab"` | `2` | `"ab"` |
| `"au"` | `2` | `"au"` |
| `" "` | `1` | `" "` |
| `"a b c"` | `3` | depending on repeated spaces/characters |
| `"123451"` | `5` | `"12345"` or `"23451"` |

A particularly useful trio for debugging is:

```text
"abba"
"dvdf"
"tmmzuxt"
```

These often expose incorrect duplicate handling.

---

# 5. Start With the Brute-Force Idea

Before optimizing, understand the simplest correct solution.

For every possible starting index:

1. create an empty set,
2. extend the substring one character at a time,
3. stop when a duplicate is found,
4. record the largest length.

Example implementation:

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0

        for start in range(len(s)):
            seen = set()

            for end in range(start, len(s)):
                if s[end] in seen:
                    break

                seen.add(s[end])
                max_length = max(max_length, end - start + 1)

        return max_length
```

## Example with `"abcabcbb"`

Starting from index `0`:

```text
a
ab
abc
abca -> duplicate a, stop
```

Starting from index `1`:

```text
b
bc
bca
bcab -> duplicate b, stop
```

Starting from index `2`:

```text
c
ca
cab
cabc -> duplicate c, stop
```

And so on.

This is correct, but inefficient.

---

# 6. Why Brute Force Is Not Good Enough

Suppose the string length is `n`.

The outer loop can run `n` times.

For each starting position, the inner loop may scan a large fraction of the string.

The total work is approximately:

\[
n + (n-1) + (n-2) + \cdots + 1
\]

Using the arithmetic-series formula:

\[
\frac{n(n+1)}{2}
\]

So the time complexity is:

\[
O(n^2)
\]

The problem with brute force is not that it checks invalid substrings.

The deeper problem is:

> It repeatedly recomputes information that we already learned.

Example:

```text
"abc"
```

is known to contain unique characters.

If the next character creates a duplicate:

```text
"abca"
```

we do **not** need to restart from scratch.

We can reuse almost the entire previous valid region.

This reuse is what sliding window gives us.

---

# 7. The Sliding-Window Insight

Suppose our current valid substring is:

```text
"abc"
```

Now another `a` arrives:

```text
"abca"
```

This is invalid because `a` appears twice.

What is the minimum amount of information we need to discard?

We do **not** need to throw away everything.

We only need to remove characters from the left until the old `a` disappears.

So:

```text
"abca"
 ^
old a
```

becomes:

```text
"bca"
```

which is valid.

This creates a moving range:

```text
s[left:right+1]
```

with two pointers:

- `left` = beginning of current valid window
- `right` = newest character being considered

The right pointer expands the window.

The left pointer shrinks the window when the uniqueness condition is violated.

---

# 8. The Window Invariant

An **invariant** is a condition that remains true at a particular point in an algorithm.

For this problem, the critical invariant is:

> After duplicate removal is finished, `s[left:right+1]` contains no repeated characters.

That means every time we calculate:

```python
right - left + 1
```

the current window is guaranteed to be valid.

This invariant is more important than memorizing the exact code.

If you understand the invariant, you can reconstruct the algorithm.

---

# 9. Set-Based Sliding-Window Solution

This is the clearest optimized solution and closely matches the implementation used in the accompanying Python file.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_len = 0
        char_set = set()
        left = 0

        for right in range(len(s)):

            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            char_set.add(s[right])

            max_len = max(max_len, right - left + 1)

        return max_len
```

Your current implementation uses exactly this core strategy:

- one set for characters in the active window,
- one `left` pointer,
- a `right` pointer driven by the loop,
- repeated shrinking with `while`,
- `right - left + 1` for window length.

---

# 10. Line-by-Line Explanation

## Initialize the best answer

```python
max_len = 0
```

This stores the largest valid window found so far.

Why not initialize it to `1`?

Because the input might be empty:

```text
s = ""
```

The correct answer is then:

```text
0
```

---

## Initialize the set

```python
char_set = set()
```

This set stores exactly the characters currently inside the active valid window.

For example, if the window is:

```text
"cab"
```

the set contains:

```python
{"c", "a", "b"}
```

The order does not matter.

We only need fast membership checking.

---

## Initialize the left pointer

```python
left = 0
```

Initially the window begins at index `0`.

The window boundaries are:

```text
left ... right
```

---

## Move the right pointer

```python
for right in range(len(s)):
```

`right` scans from left to right:

```text
0, 1, 2, 3, ..., n-1
```

Every new `right` means:

> Try to extend the current window by one character.

---

## Check whether the incoming character causes a duplicate

```python
while s[right] in char_set:
```

If `s[right]` is already in the current window, adding it would violate the invariant.

So we must shrink.

---

## Remove from the left

```python
char_set.remove(s[left])
left += 1
```

This means:

> Remove the oldest character from the current window and move the left boundary one step right.

This repeats until the incoming character is no longer duplicated.

---

## Add the incoming character

```python
char_set.add(s[right])
```

At this point:

```python
s[right] not in char_set
```

so adding it preserves uniqueness.

---

## Compute current window length

```python
right - left + 1
```

Why `+1`?

If:

```text
left = 2
right = 4
```

the included indices are:

```text
2, 3, 4
```

That is `3` elements.

Formula:

\[
4 - 2 + 1 = 3
\]

---

## Update the maximum

```python
max_len = max(max_len, right - left + 1)
```

We compare:

- best previous valid window
- current valid window

and keep the larger one.

---

## Return the answer

```python
return max_len
```

The final active window may not be the longest one.

Example:

```text
abcabcbb
```

The final valid window might be only:

```text
"b"
```

but the best window found earlier had length `3`.

Therefore we must track the maximum during the scan.

---

# 11. Why `while`, Not `if`?

This is one of the most important implementation details.

Incorrect:

```python
if s[right] in char_set:
    char_set.remove(s[left])
    left += 1
```

Correct:

```python
while s[right] in char_set:
    char_set.remove(s[left])
    left += 1
```

Why?

Because removing one character from the left may not remove the duplicated character.

Consider:

```text
s = "abba"
```

Before processing the second `b`, the current window is:

```text
"ab"
```

Set:

```python
{"a", "b"}
```

Incoming character:

```text
b
```

It is duplicated.

If we remove only one character:

```text
remove 'a'
```

the remaining window conceptually contains:

```text
"b"
```

But the incoming character is also `b`.

So the duplicate is still present.

We must remove again:

```text
remove old 'b'
```

Only then can the new `b` safely enter.

Therefore duplicate removal must continue until the constraint becomes valid again.

That requires `while`.

---

# 12. Detailed Dry Run: `abcabcbb`

Input:

```text
s = "abcabcbb"
```

Indices:

```text
index:  0 1 2 3 4 5 6 7
char:   a b c a b c b b
```

Initial state:

```text
left = 0
char_set = {}
max_len = 0
```

## Step 1

```text
right = 0
s[right] = 'a'
```

`a` is not in the set.

Add it:

```text
set = {a}
```

Window:

```text
"a"
```

Length:

```text
0 - 0 + 1 = 1
```

Update:

```text
max_len = 1
```

---

## Step 2

```text
right = 1
s[right] = 'b'
```

`b` is not in the set.

Add it.

```text
set = {a, b}
window = "ab"
```

Length:

```text
1 - 0 + 1 = 2
```

Update:

```text
max_len = 2
```

---

## Step 3

```text
right = 2
s[right] = 'c'
```

`c` is not in the set.

Add:

```text
set = {a, b, c}
window = "abc"
```

Length:

```text
2 - 0 + 1 = 3
```

Update:

```text
max_len = 3
```

---

## Step 4

```text
right = 3
s[right] = 'a'
```

Current set:

```text
{a, b, c}
```

`a` already exists.

Shrink from the left.

Remove:

```text
s[left] = s[0] = 'a'
```

Now:

```text
left = 1
set = {b, c}
```

`a` is no longer present.

Add new `a`.

```text
set = {a, b, c}
```

Current window:

```text
"bca"
```

Indices:

```text
1 ... 3
```

Length:

```text
3 - 1 + 1 = 3
```

Maximum remains `3`.

---

## Step 5

```text
right = 4
char = 'b'
```

`b` is already in the set.

Remove from left:

```text
remove s[1] = 'b'
left = 2
```

Add new `b`.

Window:

```text
"cab"
```

Length:

```text
3
```

Maximum:

```text
3
```

---

## Step 6

```text
right = 5
char = 'c'
```

Duplicate `c`.

Remove old `c`.

```text
left = 3
```

Add new `c`.

Window:

```text
"abc"
```

Length `3`.

---

## Step 7

```text
right = 6
char = 'b'
```

Current window:

```text
"abc"
```

Incoming `b` duplicates the existing `b`.

Remove `a`.

```text
window conceptually becomes "bc"
```

But `b` is still present.

So the `while` loop continues.

Remove old `b`.

Now `b` is no longer present.

Add new `b`.

Current valid window:

```text
"cb"
```

Length `2`.

Maximum remains `3`.

---

## Step 8

```text
right = 7
char = 'b'
```

Current window:

```text
"cb"
```

Incoming `b` duplicates current `b`.

Remove `c`.

Still duplicate.

Remove old `b`.

Add new `b`.

Window:

```text
"b"
```

Length `1`.

Final answer:

```text
3
```

## State Table

| `right` | char | `left` after fixing | Current valid window | `max_len` |
|---:|:---:|---:|:---|---:|
| 0 | `a` | 0 | `a` | 1 |
| 1 | `b` | 0 | `ab` | 2 |
| 2 | `c` | 0 | `abc` | 3 |
| 3 | `a` | 1 | `bca` | 3 |
| 4 | `b` | 2 | `cab` | 3 |
| 5 | `c` | 3 | `abc` | 3 |
| 6 | `b` | 5 | `cb` | 3 |
| 7 | `b` | 7 | `b` | 3 |

---

# 13. Detailed Dry Run: `abba`

This is one of the best debugging examples.

```text
index: 0 1 2 3
char:  a b b a
```

Initial:

```text
left = 0
set = {}
max = 0
```

Process `a`:

```text
window = "a"
set = {a}
max = 1
```

Process first `b`:

```text
window = "ab"
set = {a, b}
max = 2
```

Process second `b`:

```text
incoming = b
set = {a, b}
```

Duplicate detected.

Remove:

```text
a
```

State:

```text
left = 1
set = {b}
```

But incoming `b` is still in the set.

Remove again:

```text
b
```

State:

```text
left = 2
set = {}
```

Now add incoming `b`.

```text
window = "b"
```

Process final `a`:

```text
window = "ba"
```

Length `2`.

Answer:

```text
2
```

This example proves that one left-shift may not be enough.

---

# 14. Detailed Dry Run: `pwwkew`

```text
index: 0 1 2 3 4 5
char:  p w w k e w
```

Process `p`:

```text
"p"
max = 1
```

Process first `w`:

```text
"pw"
max = 2
```

Process second `w`.

Duplicate.

Remove `p`.

Still contains `w`.

Remove old `w`.

Add new `w`.

Current window:

```text
"w"
```

Continue with `k`:

```text
"wk"
```

Continue with `e`:

```text
"wke"
max = 3
```

Final `w` arrives.

Current window:

```text
"wke"
```

Incoming `w` duplicates the first character.

Remove old `w`.

Add new `w`.

New window:

```text
"kew"
```

Length `3`.

Final answer:

```text
3
```

---

# 15. Detailed Dry Run: `dvdf`

Input:

```text
d v d f
```

Process:

```text
"d"
```

then:

```text
"dv"
```

Now second `d` arrives:

```text
"dvd"
```

Duplicate `d`.

Remove only the old `d`.

Window becomes:

```text
"vd"
```

Now process `f`:

```text
"vdf"
```

Length `3`.

Answer:

```text
3
```

This example exposes an important misconception.

A wrong approach may "restart" from the duplicate and produce:

```text
"df"
```

But that throws away `v` unnecessarily.

The correct window after handling the duplicate is:

```text
"vd"
```

That retained `v` later helps form:

```text
"vdf"
```

---

# 16. Correctness Argument

A strong interview answer should explain not only that the code works, but **why**.

We can reason using the invariant.

## Invariant

After the `while` loop finishes and `s[right]` is added:

```text
s[left:right+1]
```

contains no repeated characters.

## Why is the invariant true?

Before processing `s[right]`, assume the current window is valid.

There are two cases.

### Case 1: `s[right]` is not in the current window

Then adding it cannot create a duplicate.

The new window remains valid.

### Case 2: `s[right]` is already present

The `while` loop removes characters from the left until the old occurrence of `s[right]` has been removed.

Once that happens, adding `s[right]` produces a unique-character window again.

Therefore the invariant is restored after every iteration.

## Why do we not miss the optimum?

At each `right`, after shrinking just enough to restore validity, the algorithm maintains the longest possible valid window ending at that `right`.

Any window that starts before `left` would contain the duplicated character and would therefore be invalid.

So the current valid window is the best candidate ending at `right`.

By checking every `right` and taking the maximum length, we find the globally longest valid substring.

---

# 17. Complexity Analysis

Let:

```text
n = len(s)
```

## Time Complexity

The target solution is:

\[
O(n)
\]

The `right` pointer moves from `0` to `n-1` once.

The `left` pointer also moves only forward and can advance at most `n` times.

Therefore total pointer movement is bounded by roughly:

\[
2n
\]

Constants are ignored in Big-O notation:

\[
O(2n) = O(n)
\]

## Space Complexity

The set contains characters from the active window.

In the worst case all characters are unique.

So the set may hold up to `n` characters:

\[
O(n)
\]

More precisely:

\[
O(\min(n, |\Sigma|))
\]

where \(|\Sigma|\) is the size of the character alphabet.

For a fixed character set such as ASCII, auxiliary space may be considered bounded by a constant relative to `n`, but in general interviews, saying `O(n)` space is safe.

---

# 18. Why the Nested `while` Loop Is Still O(n)

A common interview question is:

> You have a `while` loop inside a `for` loop. Why is the complexity not O(n²)?

Because the inner loop does not restart from the beginning for every `right`.

`left` only moves forward.

Example pointer movement:

```text
right:
0 -> 1 -> 2 -> 3 -> 4 -> ... -> n-1

left:
0 -> 1 -> 2 -> 3 -> ... -> n
```

Each character:

- enters the window at most once,
- leaves the window at most once.

So the total amount of work done by the inner loop across the entire execution is `O(n)`.

This is an example of **amortized analysis**.

A useful statement in an interview:

> Even though the shrinking loop is nested syntactically, each character can be removed from the window only once, so the total number of removals over the entire algorithm is at most `n`.

---

# 19. Dictionary / Last-Seen Optimization

The set solution removes characters one by one.

We can also store the most recent index of every character.

Then when a duplicate appears, we can jump `left` directly.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        max_length = 0

        for right, char in enumerate(s):

            if char in last_seen:
                left = max(left, last_seen[char] + 1)

            last_seen[char] = right

            max_length = max(
                max_length,
                right - left + 1
            )

        return max_length
```

The dictionary stores information such as:

```python
{
    "a": 0,
    "b": 1,
    "c": 2
}
```

meaning:

```text
a was most recently seen at index 0
b was most recently seen at index 1
c was most recently seen at index 2
```

If we encounter `b` again at index `4`, we can move:

```text
left
```

directly to:

```text
last_seen["b"] + 1
```

instead of deleting characters one by one.

---

# 20. Why `max(left, last_seen[c] + 1)` Matters

A common bug is:

```python
left = last_seen[char] + 1
```

without checking whether the previous occurrence lies inside the active window.

Consider:

```text
s = "abba"
```

At some point after processing the second `b`:

```text
left = 2
```

Now the final `a` appears at index `3`.

The previous `a` was at index `0`.

But index `0` lies outside the current window.

If we blindly do:

```python
left = last_seen["a"] + 1
```

we get:

```text
left = 1
```

This moves `left` backward.

That is invalid.

A sliding-window left pointer must never move backward.

Correct:

```python
left = max(left, last_seen[char] + 1)
```

For this example:

```python
left = max(2, 0 + 1)
     = max(2, 1)
     = 2
```

So the old `a` is correctly ignored.

---

# 21. Set vs Dictionary Solution

| Property | Set-Based | Dictionary-Based |
|---|---|---|
| Main structure | `set` | `dict` |
| Stores | characters in window | latest index per character |
| Duplicate handling | remove one by one | jump left directly |
| Time | `O(n)` | `O(n)` |
| Space | `O(n)` | `O(n)` |
| Beginner friendliness | excellent | moderate |
| Easy to prove | yes | yes |
| Common bug | using `if` instead of `while` | moving `left` backward |
| Good interview choice | yes | yes |
| Best for learning sliding window | **yes** | after set version |

Recommended learning order:

```text
Brute Force
    |
    v
Sliding Window + Set
    |
    v
Sliding Window + Last-Seen Dictionary
```

---

# 22. Python Implementation Guidance

## 22.1 Use a set when you only need membership

If you need to answer:

```text
"Is this character already inside my window?"
```

a set is appropriate.

```python
seen = set()
```

Operations:

```python
x in seen
seen.add(x)
seen.remove(x)
```

are `O(1)` on average.

---

## 22.2 Use `discard` only if removal may be uncertain

In this algorithm:

```python
seen.remove(s[left])
```

is safe because `s[left]` must belong to the active window.

`remove()` is appropriate.

`discard()` could also work:

```python
seen.discard(s[left])
```

but silently ignoring missing values can sometimes hide logical bugs.

For interview code, `remove()` communicates that the character should definitely exist.

---

## 22.3 Use descriptive pointer names

Prefer:

```python
left
right
```

over:

```python
i
j
```

when explaining sliding windows.

This makes the algorithm easier to communicate.

---

## 22.4 Keep the invariant visible in your code

Good structure:

```python
for right in range(len(s)):

    while window_invalid:
        shrink_from_left()

    add_right_character()

    update_answer()
```

This mirrors the reasoning.

---

## 22.5 Avoid slicing inside the main loop

Do not repeatedly write:

```python
current = s[left:right+1]
```

just to calculate length.

String slicing creates a new string and costs additional time.

Use:

```python
right - left + 1
```

instead.

You may slice only if the interviewer asks for the actual substring.

---

## 22.6 LeetCode method name

For direct LeetCode submission, the expected signature is normally:

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        ...
```

If practicing locally, using a more descriptive custom method name is fine, but be ready to adapt to the platform signature.

---

# 23. Common Mistakes

## Mistake 1 — Using `if` instead of `while`

Wrong:

```python
if s[right] in seen:
    seen.remove(s[left])
    left += 1
```

Counterexample:

```text
"abba"
```

Correct:

```python
while s[right] in seen:
    seen.remove(s[left])
    left += 1
```

---

## Mistake 2 — Forgetting `+1`

Wrong:

```python
right - left
```

Correct:

```python
right - left + 1
```

Because both boundaries are inclusive.

---

## Mistake 3 — Clearing the entire set

Wrong strategy:

```python
if duplicate:
    seen.clear()
```

This discards too much useful information.

For:

```text
"dvdf"
```

when the second `d` arrives, `v` should remain available.

---

## Mistake 4 — Restarting from the duplicate

For:

```text
"dvdf"
```

a wrong mental model gives:

```text
"d" -> "dv" -> duplicate -> restart at "d" -> "df"
```

and incorrectly misses:

```text
"vdf"
```

Sliding window says:

```text
remove only what is necessary
```

not:

```text
restart everything
```

---

## Mistake 5 — Confusing substring with subsequence

`"pwke"` from `"pwwkew"` is not contiguous.

Therefore it cannot be used.

---

## Mistake 6 — Moving `left` backward in the dictionary version

Wrong:

```python
left = last_seen[char] + 1
```

Correct:

```python
left = max(left, last_seen[char] + 1)
```

---

## Mistake 7 — Updating the answer before restoring validity

Wrong ordering:

```python
max_length = max(max_length, right - left + 1)

while duplicate:
    ...
```

At that moment the measured window may contain duplicates.

Correct ordering:

```text
expand
shrink until valid
measure
```

---

## Mistake 8 — Using a list instead of a set

This works functionally:

```python
if char in current_chars:
```

but membership in a list is `O(k)` rather than average `O(1)`.

That can degrade performance.

---

## Mistake 9 — Returning the final window length

The final window may not be the maximum.

Always maintain:

```python
max_length
```

---

# 24. Edge Cases

## Empty string

```text
Input: ""
Output: 0
```

No iterations occur.

---

## One character

```text
Input: "x"
Output: 1
```

---

## All identical

```text
Input: "aaaaaa"
Output: 1
```

---

## All unique

```text
Input: "abcdef"
Output: 6
```

`left` never moves.

---

## Duplicate at the end

```text
Input: "abcdea"
Output: 5
```

---

## Duplicate near the beginning

```text
Input: "aabcdef"
Output: 7
```

Longest valid substring:

```text
"abcdef"
```

Actually length `6` for this exact input. This is a good reminder to manually verify test expectations rather than trusting intuition.

---

## Spaces

```text
Input: "a b a"
```

Spaces are characters and count in the uniqueness constraint.

---

## Digits and symbols

```text
Input: "a1!b2@"
Output: 6
```

The algorithm does not care whether characters are letters.

---

## Unicode characters

Python strings support Unicode.

The same logic works for strings containing many non-ASCII characters, although the exact interpretation of "character" can become nuanced for certain composed Unicode sequences. For standard coding-interview assumptions, Python string iteration is sufficient.

---

# 25. How to Explain This in an Interview

A polished explanation:

> I would use a variable-size sliding window. The window is represented by `left` and `right`, and I maintain a set containing the characters currently inside the window. I expand the right boundary one character at a time. If the incoming character is already present, the uniqueness constraint is violated, so I repeatedly remove characters from the left and advance `left` until the duplicate disappears. Then I add the incoming character and update the maximum window length. The window is always unique when I measure it. Each character enters and leaves the window at most once, so the time complexity is O(n), with O(n) auxiliary space in the general case.

If asked for an optimization:

> Instead of a set, I can store the most recent index of every character in a dictionary. When a duplicate appears, I jump `left` directly to one position after the previous occurrence, while ensuring `left` never moves backward.

---

# 26. How to Recognize Sliding-Window Problems

Look for combinations of words such as:

```text
longest substring
shortest substring
minimum window
maximum subarray
contiguous
at most K
at least K
without repeating
contains all
sum less than
sum greater than
exactly K distinct
```

Especially suspicious structure:

> Find the longest/shortest contiguous region satisfying some constraint.

Then ask:

1. Can I expand one boundary?
2. Can I detect when the constraint becomes invalid?
3. Can I restore validity by moving the other boundary?
4. Can the pointers move monotonically forward?

If yes, sliding window is likely applicable.

---

# 27. Generic Sliding-Window Templates

## Variable-size window

```python
left = 0

for right in range(len(data)):

    add(data[right])

    while window_is_invalid():
        remove(data[left])
        left += 1

    update_answer(left, right)
```

For LeetCode 3, we must check duplication before adding `s[right]` in the set-based formulation:

```python
seen = set()
left = 0
answer = 0

for right in range(len(s)):

    while s[right] in seen:
        seen.remove(s[left])
        left += 1

    seen.add(s[right])

    answer = max(answer, right - left + 1)
```

## Frequency-map template

Many harder sliding-window problems require counts:

```python
from collections import defaultdict

freq = defaultdict(int)
left = 0

for right in range(len(data)):
    freq[data[right]] += 1

    while constraint_is_violated(freq):
        freq[data[left]] -= 1
        left += 1

    update_answer()
```

This is the natural next step after LeetCode 3.

---

# 28. Interview Questions — Easy

These are designed to test whether the candidate understands the fundamentals rather than just memorizing code.

## Q1. What is the difference between a substring and a subsequence?

**Answer:**

A substring must be contiguous in the original string. A subsequence preserves order but may skip characters.

For:

```text
"pwwkew"
```

`"wke"` is a substring.

`"pwke"` can be a subsequence but is not a substring.

---

## Q2. Why is a set useful in this problem?

**Answer:**

The algorithm repeatedly needs to know whether the incoming character already exists in the current window. A hash set supports average `O(1)` membership checks, insertions, and removals.

---

## Q3. What do `left` and `right` represent?

**Answer:**

They are the inclusive boundaries of the active sliding window:

```python
s[left:right+1]
```

`right` expands the window.

`left` shrinks it when the uniqueness constraint is violated.

---

## Q4. Why is the window length `right - left + 1`?

**Answer:**

Because both endpoints are included.

For indices `2` through `4`, the characters are at positions:

```text
2, 3, 4
```

There are `3` characters:

\[
4-2+1=3
\]

---

## Q5. Why can we initialize `max_length = 0`?

**Answer:**

Because the string may be empty. The longest valid substring of an empty string has length `0`.

---

## Q6. What condition makes the current window invalid?

**Answer:**

The incoming character already exists inside the active window, which would create a repeated character.

---

## Q7. Why do we shrink from the left instead of from the right?

**Answer:**

`right` represents the newest character we are trying to include. We want to preserve it and find the longest valid substring ending at `right`. Therefore we discard only as much old information as necessary from the left.

---

## Q8. Why not restart from scratch after finding a duplicate?

**Answer:**

Because much of the previous window may still be useful.

For:

```text
"dvdf"
```

when the second `d` appears, `"v"` remains valid and helps produce `"vdf"`.

Restarting would lose useful information and make the solution less efficient.

---

## Q9. What is the output for `"bbbbb"`?

**Answer:**

```text
1
```

Every valid substring can contain at most one `b`.

---

## Q10. What is the output for an empty string?

**Answer:**

```text
0
```

---

## Q11. What happens if every character is unique?

**Answer:**

`left` never moves.

The window expands across the entire string, and the answer is the string length.

---

## Q12. Why use `while` instead of `if`?

**Answer:**

One removal may not remove the duplicated character.

`"abba"` is the standard counterexample.

When the second `b` arrives, removing only `a` is insufficient because old `b` is still in the window.

---

## Q13. What is the space complexity?

**Answer:**

`O(n)` in the general case because the set may contain up to `n` unique characters.

More precisely:

\[
O(\min(n, |\Sigma|))
\]

---

## Q14. Can spaces be duplicated characters?

**Answer:**

Yes.

A space is a character just like a letter, digit, or symbol.

---

## Q15. Does case matter?

**Answer:**

Yes, under ordinary string comparison:

```text
"A" != "a"
```

So `"Aa"` contains two distinct characters.

---

# 29. Interview Questions — Medium

These questions are closer to what product-company technical interviews use to distinguish understanding from memorization.

## Q1. Why is the algorithm O(n) even though there is a nested `while` loop?

**Answer:**

Because the left pointer never moves backward.

The right pointer advances `n` times.

Across the full execution, the left pointer can also advance at most `n` times.

Therefore total pointer movement is bounded by `2n`, giving `O(n)` time.

This is amortized analysis.

---

## Q2. State the invariant maintained by the sliding window.

**Answer:**

After duplicate removal and insertion of the right character:

```python
s[left:right+1]
```

contains no repeated characters.

This invariant makes the current length safe to use as a candidate answer.

---

## Q3. Why is the current window the longest valid substring ending at `right`?

**Answer:**

When duplication occurs, the algorithm moves `left` only until the duplicate disappears.

Any smaller movement would leave the window invalid.

Any larger movement would unnecessarily shorten the window.

Therefore after shrinking, the window is the longest valid one ending at the current `right`.

---

## Q4. Can you solve the problem with a dictionary?

**Answer:**

Yes.

Store the most recent index of every character.

When a duplicate appears, jump `left` directly:

```python
left = max(left, last_seen[char] + 1)
```

Then update:

```python
last_seen[char] = right
```

This also runs in `O(n)` time.

---

## Q5. Why is `max(left, last_seen[char] + 1)` necessary?

**Answer:**

Because the previous occurrence may lie outside the current window.

Without `max`, `left` could move backward.

Example:

```text
"abba"
```

After the duplicate `b`, `left` becomes `2`.

The old `a` at index `0` should not move `left` back to `1`.

---

## Q6. Which version would you prefer in an interview: set or dictionary?

**Answer:**

The set version is often easier to derive, explain, and prove.

The dictionary version can be slightly cleaner and avoids repeated left removals by jumping directly.

Both are asymptotically optimal.

A strong candidate should be able to explain both.

---

## Q7. Can the algorithm return the actual substring instead of only the length?

**Answer:**

Yes.

Track the starting position whenever a new maximum is found.

```python
best_start = 0
best_length = 0

if current_length > best_length:
    best_length = current_length
    best_start = left
```

Then return:

```python
s[best_start:best_start + best_length]
```

---

## Q8. How would you return all longest substrings?

**Answer:**

Track:

- current maximum length,
- a collection of windows whose length equals that maximum.

If a larger window appears, clear the collection and store the new one.

If an equal-length window appears, add it.

Be careful whether the interviewer wants unique substring values or unique index intervals.

---

## Q9. How would the algorithm change if the question asked for at most `K` distinct characters?

**Answer:**

Use a frequency dictionary rather than a set.

Expand right and increase the incoming character count.

While:

```text
number of distinct characters > K
```

decrease counts from the left.

Delete a character from the dictionary when its count becomes zero.

This is the pattern behind LeetCode 340.

---

## Q10. Why is a frequency map unnecessary for the original problem?

**Answer:**

The set-based implementation maintains a window where every character occurs at most once, so presence/absence is sufficient.

We do not need exact counts because duplicates are removed immediately.

---

## Q11. Can you solve the problem using an array instead of a dictionary?

**Answer:**

Yes, if the character domain is bounded.

For ASCII, an array indexed by character code can store last-seen positions.

Example:

```python
last = [-1] * 128
```

This can reduce hash-table overhead but is less general than a dictionary.

---

## Q12. Why should you avoid repeatedly slicing the string inside the loop?

**Answer:**

A slice such as:

```python
s[left:right+1]
```

creates a new string.

Doing this every iteration adds unnecessary time and memory overhead.

For length, compute:

```python
right - left + 1
```

directly.

---

## Q13. What would happen if we updated `max_length` before shrinking?

**Answer:**

We might measure an invalid window containing duplicate characters and produce an incorrect answer.

The correct order is:

```text
expand
restore validity
measure
```

---

## Q14. Why is the final window not necessarily the answer?

**Answer:**

The best window may occur earlier.

For:

```text
"abcabcbb"
```

the answer is `3`, even though the final valid window can have length `1`.

Therefore we keep a global maximum.

---

## Q15. Can this be solved in place with O(1) extra memory?

**Answer:**

Only if the character alphabet is treated as fixed and bounded, allowing a constant-size array.

For arbitrary input symbols, information about previously seen characters must be stored, so auxiliary space depends on the number of distinct characters.

---

## Q16. What is amortized analysis in the context of this problem?

**Answer:**

A single iteration may perform many left-pointer movements, but those movements cannot repeat indefinitely.

Every element can leave the window only once.

So expensive-looking individual iterations are balanced by cheap ones, and total work remains linear.

---

## Q17. Is binary search useful here?

**Answer:**

It is possible to binary-search a candidate length and test whether a unique substring of that length exists, but that is more complicated and generally gives worse complexity than the direct `O(n)` sliding-window solution.

Sliding window exploits the structure more naturally.

---

## Q18. Is a two-pointer solution always a sliding-window solution?

**Answer:**

No.

Two pointers is a broader technique.

Examples include:

- opposite-end pointers in sorted arrays,
- fast/slow pointers in linked lists,
- partitioning,
- merge-style scans.

Sliding window is a specific two-pointer pattern where the pointers bound a contiguous active region.

---

## Q19. What property allows `left` to move monotonically?

**Answer:**

Once a starting position becomes impossible because it creates a duplicate with the current or later right boundary, there is no reason to revisit earlier discarded positions for the current scan.

This monotonicity is central to linear complexity.

---

## Q20. Why is LeetCode 3 considered a foundational sliding-window problem?

**Answer:**

Because it contains the full variable-window structure in one of its simplest forms:

- expand right,
- detect constraint violation,
- shrink left until valid,
- update optimum.

The same framework generalizes to frequency constraints, sums, counts, replacement budgets, and target coverage.

---

# 30. Interview Questions — Difficult

These questions focus on proof, variants, implementation trade-offs, and deeper reasoning.

## Q1. Prove that no optimal substring is skipped when `left` advances.

**Answer:**

Suppose the incoming character at `right` duplicates a character already inside the window at position `p`.

Any substring ending at `right` and starting at or before `p` contains both copies of that character and is invalid.

Therefore all start positions:

```text
<= p
```

can be discarded.

Moving `left` beyond the old occurrence cannot eliminate a valid candidate ending at `right`, because none of those earlier starts were valid.

---

## Q2. Why is the set solution still optimal even though the dictionary solution can jump farther?

**Answer:**

Both are `O(n)` asymptotically.

The set version may perform multiple constant-time removals during one iteration, but each character is removed at most once overall.

The dictionary version improves the constant factor in some cases by updating `left` directly, but it does not improve Big-O complexity.

---

## Q3. How would you adapt this for a streaming character source where the full string is not stored?

**Answer:**

If only the maximum length is needed:

- maintain the current window state,
- maintain a set or last-seen dictionary,
- maintain a logical index for incoming characters.

For the set version, removing the leftmost character requires knowing which character is leaving, so the active window itself must be stored in a queue/deque.

For a last-seen dictionary version, a logical `left` index and latest positions may be enough for the length calculation, depending on requirements.

---

## Q4. What happens if character hashing becomes pathological?

**Answer:**

Hash-based structures are expected `O(1)` average time, not strict worst-case `O(1)` for all theoretical models.

A bounded-alphabet array avoids hashing and gives deterministic constant-time indexing.

In normal Python interview analysis, set/dictionary operations are treated as average `O(1)`.

---

## Q5. Can you formulate the problem as finding the longest interval satisfying a predicate?

**Answer:**

Yes.

We seek the maximum-length interval:

\[
[L,R]
\]

such that:

\[
\forall c,\quad \text{freq}_{L,R}(c) \le 1
\]

The sliding window works because when the predicate becomes false due to the new right endpoint, removing elements from the left can restore it.

---

## Q6. What monotonicity property does the problem exploit?

**Answer:**

For a fixed right endpoint, if a window contains a duplicate, expanding it further left cannot restore uniqueness.

To restore validity, the left boundary must move right.

This one-directional correction enables monotonic pointers.

---

## Q7. Could you use a frequency dictionary and maintain `duplicate_count`?

**Answer:**

Yes.

You could increment character counts as the window expands and maintain how many characters have frequency greater than one.

Then shrink while:

```text
duplicate_count > 0
```

This is more general but unnecessarily complex for this problem.

It becomes useful in variants with richer constraints.

---

## Q8. How would you handle the variant: longest substring where every character appears at most twice?

**Answer:**

Use a frequency dictionary.

Expand right:

```python
freq[s[right]] += 1
```

While:

```python
freq[s[right]] > 2
```

shrink from the left:

```python
freq[s[left]] -= 1
left += 1
```

Then update the maximum.

---

## Q9. How would you handle the variant: exactly K distinct characters?

**Answer:**

A standard strategy is to derive:

```text
count(exactly K)
=
count(at most K)
-
count(at most K-1)
```

for counting problems.

For longest-length problems, maintain a window with at most `K` distinct characters and update the answer only when the window has exactly `K`.

---

## Q10. Why is "longest substring without repeating characters" easier than "minimum window substring"?

**Answer:**

LeetCode 3 has a local validity rule:

```text
all frequencies <= 1
```

and validity can be restored by removing characters until the duplicate disappears.

Minimum Window Substring requires satisfying multiplicities of a target pattern and carefully deciding when the window is sufficiently covered before minimizing it.

The bookkeeping is more complex.

---

## Q11. Could dynamic programming solve this problem?

**Answer:**

Yes, one can define the length of the longest unique suffix ending at each position and use last-seen indices.

However, the resulting recurrence is essentially another formulation of sliding-window / last-seen reasoning.

Sliding window is more direct and usually clearer.

---

## Q12. Derive a recurrence for the dictionary approach.

**Answer:**

Let:

```text
L_r
```

be the smallest valid left boundary for a unique substring ending at position `r`.

If character `s[r]` was previously seen at `p`, then:

\[
L_r = \max(L_{r-1}, p+1)
\]

Otherwise:

\[
L_r = L_{r-1}
\]

The candidate length is:

\[
r - L_r + 1
\]

This is exactly the last-seen dictionary algorithm.

---

## Q13. Why can the previous occurrence of a character outside the active window be ignored?

**Answer:**

Uniqueness only concerns characters inside the current interval.

If:

```text
last_seen[c] < left
```

then that occurrence is not part of:

```text
s[left:right]
```

so adding `c` does not duplicate anything inside the active window.

---

## Q14. Suppose the input alphabet contains only lowercase English letters. How can you optimize space?

**Answer:**

Use a fixed array of size `26`.

For last-seen positions:

```python
last = [-1] * 26
index = ord(char) - ord('a')
```

This gives `O(1)` auxiliary space relative to input size.

---

## Q15. How would you return the lexicographically smallest substring among all maximum-length valid substrings?

**Answer:**

First find the maximum length.

While scanning, whenever a valid window reaches that length:

- compare its substring with the best lexicographic candidate,
- keep the smaller one.

For performance-sensitive cases, avoid repeated full slicing/comparison if large strings are involved; more advanced string-comparison methods may be appropriate.

---

## Q16. How would you count the number of substrings with no repeating characters?

**Answer:**

At every `right`, after restoring uniqueness, every substring ending at `right` and starting anywhere from `left` through `right` is unique.

The number of valid substrings ending at `right` is:

\[
right-left+1
\]

So accumulate:

```python
count += right - left + 1
```

This converts a maximum-length problem into a counting problem using the same invariant.

---

## Q17. Why does that counting formula work?

**Answer:**

Once:

```text
s[left:right+1]
```

is unique, every suffix of that window is also unique.

Those suffixes start at:

```text
left, left+1, ..., right
```

There are exactly:

\[
right-left+1
\]

of them.

---

## Q18. How would you parallelize this algorithm?

**Answer:**

The standard sliding-window algorithm is inherently sequential because the valid left boundary for position `right` depends on previous characters.

You can split input into blocks, but substrings crossing block boundaries require extra boundary-state reconciliation, which complicates the approach and usually defeats the simplicity of the linear scan.

For ordinary interview constraints, sequential `O(n)` is the appropriate solution.

---

## Q19. Why does sorting not help?

**Answer:**

Sorting destroys the original order and contiguity.

The problem is about substrings, so positional structure is essential.

---

## Q20. Can this be generalized to arrays?

**Answer:**

Yes.

Nothing in the algorithm fundamentally requires strings.

For an array:

```python
[1, 2, 3, 2, 4]
```

the exact same technique finds the longest contiguous subarray of distinct values.

---

## Q21. What is the deepest reusable lesson from this problem?

**Answer:**

Do not recompute a contiguous candidate from scratch when a local change makes it invalid.

Instead:

1. preserve the valid state you already have,
2. remove only the minimum information needed to restore the invariant,
3. continue scanning monotonically.

That principle is the heart of sliding-window optimization.

---

## Q22. If the interviewer asks for strict worst-case rather than average hash complexity, what can you say?

**Answer:**

For a fixed known alphabet, replace hashing with an indexed array.

For arbitrary symbols, balanced-tree structures can give `O(log k)` worst-case operations, leading to `O(n log k)` time, where `k` is the number of distinct active symbols.

In practical Python interview analysis, dict/set are normally considered average `O(1)`.

---

## Q23. Why is the dictionary solution sometimes described as "optimized sliding window" even though both versions are O(n)?

**Answer:**

Because it may reduce the number of individual operations.

The set version can move `left` several steps in one right-pointer iteration.

The dictionary version can calculate the necessary new `left` directly.

This is a constant-factor and implementation-level optimization, not an asymptotic improvement.

---

## Q24. How would you test whether a candidate truly understands the invariant?

**Answer:**

Ask them to explain:

```text
Why is the window guaranteed valid when max_length is updated?
```

A memorized answer often focuses only on code.

A real understanding explains the sequence:

```text
duplicate detected
-> left characters removed
-> duplicate eliminated
-> incoming character added
-> invariant restored
-> length measured
```

---

## Q25. What is the relationship between this problem and finite-state incremental processing?

**Answer:**

Instead of recomputing properties of every substring independently, the algorithm maintains a compact state describing the current candidate:

- left boundary,
- right boundary,
- set/dictionary state,
- best answer.

Each incoming character produces a small state transition.

This incremental-state viewpoint is useful far beyond sliding windows.

---

# 31. Follow-Up Variations an Interviewer May Ask

## Variation 1 — Return the substring

Example:

```text
Input: "abcabcbb"
Output: "abc"
```

Track:

```python
best_start
best_length
```

---

## Variation 2 — Return all longest unique substrings

Example:

```text
Input: "abcabcbb"
Possible result:
["abc", "bca", "cab"]
```

Clarify whether duplicate values should be returned once or once per occurrence.

---

## Variation 3 — Longest substring with at most K distinct characters

Use a frequency map.

Related problem:

```text
LeetCode 340
```

---

## Variation 4 — Longest substring after at most K replacements

Related problem:

```text
LeetCode 424
```

Requires maintaining the frequency of the most common character in the window.

---

## Variation 5 — Minimum window containing all characters of another string

Related problem:

```text
LeetCode 76
```

This is a much more advanced frequency-map sliding-window problem.

---

## Variation 6 — Longest subarray with distinct integers

Same algorithm, but input is an integer array.

---

## Variation 7 — Every character may appear at most twice

Replace the set with a frequency map.

---

## Variation 8 — Count all unique-character substrings

Accumulate:

```python
right - left + 1
```

after each valid-window restoration.

---

# 32. Similar LeetCode Problems

The following sequence is useful for mastering sliding windows.

## Closest Conceptual Problems

### LeetCode 159 — Longest Substring with At Most Two Distinct Characters

Core extension:

```text
unique characters -> at most two distinct characters
```

Use a frequency map.

---

### LeetCode 340 — Longest Substring with At Most K Distinct Characters

Generalization of 159.

Key concept:

```text
while number_of_distinct_characters > k:
    shrink
```

---

### LeetCode 424 — Longest Repeating Character Replacement

Find the longest substring that can be made uniform after at most `k` replacements.

Important invariant:

```text
window_size - max_frequency <= k
```

---

### LeetCode 567 — Permutation in String

Fixed-size sliding window.

Tests whether one string has a permutation appearing inside another.

---

### LeetCode 438 — Find All Anagrams in a String

Another fixed-size frequency-window problem.

---

### LeetCode 76 — Minimum Window Substring

One of the most important advanced sliding-window problems.

Requires:

- target frequencies,
- window frequencies,
- formed/required bookkeeping,
- expanding to satisfy,
- shrinking to minimize.

---

### LeetCode 1004 — Max Consecutive Ones III

Array version of variable-size sliding window.

Constraint:

```text
at most k zeros
```

---

### LeetCode 904 — Fruit Into Baskets

Equivalent to:

```text
longest subarray with at most 2 distinct values
```

---

### LeetCode 209 — Minimum Size Subarray Sum

Sliding window over positive numbers.

Goal:

```text
smallest window with sum >= target
```

---

### LeetCode 713 — Subarray Product Less Than K

Variable-size sliding window over positive integers.

---

### LeetCode 1208 — Get Equal Substrings Within Budget

Window cost must remain within a budget.

---

### LeetCode 1456 — Maximum Number of Vowels in a Substring of Given Length

Fixed-size window.

Excellent beginner exercise after LeetCode 3.

---

### LeetCode 3 — Longest Substring Without Repeating Characters

This problem should serve as your fundamental variable-window template.

---

# 33. Non-LeetCode Practice Problems

These exercises are deliberately written in interview style.

Do not immediately search for solutions.

Try to identify:

```text
window state
validity condition
when to shrink
what answer to update
```

---

## Exercise 1 — Longest Unique Integer Segment

Given an integer array, return the length of the longest contiguous subarray containing no repeated values.

### Example

```text
Input:
[1, 2, 3, 1, 2, 4, 5]

Output:
5
```

One longest valid segment:

```text
[3, 1, 2, 4, 5]
```

### Test Cases

```text
[] -> 0
[1] -> 1
[1,1,1] -> 1
[1,2,3] -> 3
[1,2,1,3,4] -> 4
```

**Hint:** This is LeetCode 3 with integers.

---

## Exercise 2 — Longest Segment With At Most Two Categories

Given an array of category IDs, return the longest contiguous segment containing at most two distinct categories.

### Example

```text
Input:
[A, B, A, C, C, B]

Output:
3
```

Possible longest windows include:

```text
[A, B, A]
[A, C, C]
[C, C, B]
```

### Test Cases

```text
[] -> 0
[A] -> 1
[A,A,A] -> 3
[A,B,C] -> 2
[A,B,A,B,B] -> 5
```

**Hint:** Frequency map + number of distinct keys.

---

## Exercise 3 — Longest Substring With No Character Appearing More Than Twice

### Example

```text
Input:
"aaabbc"

Output:
5
```

One valid substring:

```text
"aabbc"
```

### Test Cases

```text
"" -> 0
"a" -> 1
"aaa" -> 2
"aabbcc" -> 6
"abacada" -> ?
```

**Hint:** Replace the set with character counts.

---

## Exercise 4 — Count All Unique-Character Substrings

Return the total number of substrings containing no repeated characters.

### Example

```text
Input:
"abc"

Output:
6
```

Valid substrings:

```text
"a"
"b"
"c"
"ab"
"bc"
"abc"
```

### Test Cases

```text
"" -> 0
"a" -> 1
"aa" -> 2
"ab" -> 3
"aba" -> 5
```

**Hint:** After restoring validity at each `right`, add:

```python
right - left + 1
```

---

## Exercise 5 — Longest Log Window With Unique User IDs

You receive chronological login events as user IDs.

Find the longest consecutive event interval in which no user appears twice.

### Example

```text
Input:
[42, 17, 8, 42, 9, 10]

Output:
5
```

Longest window:

```text
[17, 8, 42, 9, 10]
```

### Test Cases

```text
[1] -> 1
[1,1] -> 1
[1,2,3,4] -> 4
[1,2,1,2] -> 2
```

---

## Exercise 6 — Longest Sequence With At Most K Duplicate Events

Given an array and integer `k`, find the longest contiguous segment containing at most `k` positions whose values repeat an earlier value inside that same segment.

This is intentionally more difficult.

You must define carefully what counts as a "duplicate event" and maintain suitable frequency state.

### Example

```text
Input:
arr = [1,2,1,3,2]
k = 1
```

Work through the definition manually before coding.

---

## Exercise 7 — Smallest Window Containing K Distinct Characters

Given a string and integer `k`, return the length of the shortest substring containing at least `k` distinct characters.

### Example

```text
Input:
s = "aabcbcdbca"
k = 3

Output:
3
```

For example:

```text
"abc"
```

### Test Cases

```text
("abc", 1) -> 1
("abc", 3) -> 3
("aaaa", 2) -> impossible
```

**Hint:** This reverses the optimization objective. Expand until valid, then shrink while still valid.

---

## Exercise 8 — Longest Substring Under Character Cost Budget

Each character has a cost.

Given:

```python
cost = {
    'a': 1,
    'b': 2,
    'c': 4
}
```

and budget `B`, find the longest substring whose total cost does not exceed `B`.

### Example

```text
s = "abac"
B = 5
```

Determine the longest valid contiguous substring.

**Hint:** Maintain running window cost.

---

## Exercise 9 — Longest Distinct Word Span

Given a sentence tokenized into words, find the longest contiguous sequence of words without repeating a word.

### Example

```text
Input:
["the", "cat", "saw", "the", "dog"]

Output:
4
```

One longest span:

```text
["cat", "saw", "the", "dog"]
```

This tests whether you understand that the algorithm works on arbitrary hashable values, not only characters.

---

## Exercise 10 — Return the Indices of the Best Window

Given a string, return:

```text
(start_index, end_index)
```

of one longest substring with unique characters.

### Example

```text
Input:
"pwwkew"

Possible Output:
(2, 4)
```

corresponding to:

```text
"wke"
```

### Test Cases

```text
"" -> define expected convention
"a" -> (0,0)
"abc" -> (0,2)
"abba" -> (0,1) or (2,3)
```

Clarify tie-breaking rules in an interview.

---

## Exercise 11 — Earliest Maximum Unique Window

Return the earliest longest unique-character substring.

### Example

```text
Input:
"abcabcbb"

Output:
"abc"
```

Because multiple longest substrings have length `3`, but `"abc"` beginning at index `0` is earliest.

---

## Exercise 12 — Latest Maximum Unique Window

Same as Exercise 11, but choose the latest starting position among ties.

This tests careful update conditions:

```python
>
```

versus:

```python
>=
```

when updating the best answer.

---

# 34. Test Strategy

A strong engineer does not test only the happy path.

Use categories.

## Category A — Empty / minimal input

```text
""
"a"
```

## Category B — All repeated

```text
"aaaaaa"
"bbbb"
```

## Category C — All unique

```text
"abcdef"
"123456"
```

## Category D — Duplicate immediately

```text
"aab"
"aa"
```

## Category E — Duplicate after a longer prefix

```text
"abcdea"
```

## Category F — Requires multiple left movements

```text
"abba"
"pwwkew"
```

## Category G — Must preserve part of the previous window

```text
"dvdf"
```

## Category H — Best answer appears before the end

```text
"abcabcbb"
```

## Category I — Spaces / punctuation

```text
"a b"
"a!b!c"
```

## Category J — Mixed case

```text
"AaBbA"
```

A good test suite attacks the assumptions behind the implementation.

---

# 35. Debugging Checklist

If your output is wrong, ask these in order.

## 1. Am I solving substring, not subsequence?

The candidate must be contiguous.

## 2. Is my window valid when I measure it?

If not, move answer update after shrinking.

## 3. Did I use `while` instead of `if`?

Test:

```text
"abba"
```

## 4. Did I calculate length with `+1`?

Correct:

```python
right - left + 1
```

## 5. Does `left` ever move backward?

It must not.

For the dictionary solution, use:

```python
left = max(left, last_seen[c] + 1)
```

## 6. Am I clearing too much state?

Do not restart the whole window unnecessarily.

## 7. Am I returning the best length, not just the final length?

Track a global maximum.

## 8. Is the set synchronized with the active window?

Every character removed from the left must also be removed from the set.

## 9. Did I accidentally add the new character before handling duplication?

If using the set version shown here, remove duplicates first, then add.

---

# 36. Pattern Recognition Cheat Sheet

When you see:

```text
Longest + contiguous + condition
```

think:

```text
variable sliding window
```

When you see:

```text
Exactly K consecutive positions
```

think:

```text
fixed-size sliding window
```

When you see:

```text
Need fast "is this present?"
```

think:

```text
set
```

When you see:

```text
Need counts per value
```

think:

```text
frequency dictionary
```

When you see:

```text
Need previous position
```

think:

```text
last-seen dictionary
```

For LeetCode 3 specifically:

```text
State:
    set of characters

Expand:
    right += 1

Invalid when:
    s[right] already in set

Repair:
    remove s[left]
    left += 1
    repeat until valid

Answer:
    max(right - left + 1)
```

---

# 37. Practice Roadmap

A useful order for mastering this pattern:

## Stage 1 — Understand unique-window mechanics

1. LeetCode 3 — Longest Substring Without Repeating Characters
2. Longest distinct integer subarray
3. Count all distinct-character substrings

## Stage 2 — Frequency maps

4. LeetCode 159 — At Most Two Distinct Characters
5. LeetCode 340 — At Most K Distinct Characters
6. LeetCode 904 — Fruit Into Baskets

## Stage 3 — Budget constraints

7. LeetCode 1004 — Max Consecutive Ones III
8. LeetCode 424 — Longest Repeating Character Replacement
9. LeetCode 1208 — Get Equal Substrings Within Budget

## Stage 4 — Fixed-size windows

10. LeetCode 1456 — Maximum Number of Vowels
11. LeetCode 567 — Permutation in String
12. LeetCode 438 — Find All Anagrams in a String

## Stage 5 — Advanced minimum windows

13. LeetCode 209 — Minimum Size Subarray Sum
14. LeetCode 76 — Minimum Window Substring

Do not memorize each problem independently.

Try to identify the same skeleton underneath them.

---

# 38. Final Takeaways

The key idea is not:

```text
"Remember this code."
```

The key idea is:

```text
Maintain a valid contiguous window
and change it incrementally.
```

For LeetCode 3:

1. `right` expands the candidate substring.
2. A set tells us whether the new character creates a duplicate.
3. If the window becomes invalid, move `left` forward.
4. Remove only as much as necessary.
5. Once valid again, compute:

```python
right - left + 1
```

6. Track the maximum over all right endpoints.

The core implementation is:

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        max_length = 0

        for right in range(len(s)):

            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])

            max_length = max(
                max_length,
                right - left + 1
            )

        return max_length
```

Time:

\[
O(n)
\]

Space:

\[
O(n)
\]

The mental model to remember is:

```text
EXPAND RIGHT
      |
      v
CONSTRAINT BROKEN?
      |
     YES
      |
      v
SHRINK LEFT UNTIL VALID
      |
      v
UPDATE BEST ANSWER
```

Once this pattern becomes automatic, a large family of substring and subarray interview questions becomes much easier to reason about.

---

# Compact Interview Revision Sheet

Before an interview, remember these five points:

```text
1. Window = s[left:right+1]

2. Invariant:
   no duplicate characters inside the valid window

3. Duplicate:
   shrink from left until duplicate disappears

4. Length:
   right - left + 1

5. Complexity:
   O(n), because both pointers only move forward
```

And remember the two classic traps:

```text
"abba"
```

tests whether you understand why shrinking may require multiple steps.

```text
"dvdf"
```

tests whether you understand why you should preserve useful characters instead of restarting the window.

If you can explain those two cases clearly, derive the set solution without memorization, justify `O(n)` using monotonic pointers, and explain the last-seen dictionary optimization, you understand this problem at interview level.
