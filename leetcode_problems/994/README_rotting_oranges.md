# LeetCode 994 — Rotting Oranges

## Problem Type

- **Primary topic:** Graphs / Breadth-First Search
- **Core pattern:** Multi-source BFS
- **Secondary topics:** Grid traversal, simulation, shortest path in unweighted graphs
- **Difficulty:** Medium
- **LeetCode:** 994 — Rotting Oranges

---

# 1. Problem Statement

You are given an `m x n` grid where every cell contains one of three values:

- `0` → an empty cell
- `1` → a fresh orange
- `2` → a rotten orange

Every minute, any fresh orange that is directly adjacent to a rotten orange becomes rotten.

Adjacency is only in the four cardinal directions:

- up
- down
- left
- right

Diagonal cells do **not** count.

Return the **minimum number of minutes** that must elapse until no fresh orange remains.

If some fresh orange can never become rotten, return `-1`.

---

# 2. Why This Problem Matters

Rotting Oranges is one of the most important introductory problems for learning **multi-source BFS**.

The same pattern appears in problems involving:

- infection spread
- fire propagation
- flood expansion
- distance to nearest source
- contamination spread
- shortest travel time in grids
- nearest hospital / gate / charging station
- wave-front propagation
- simultaneous processes starting from multiple locations

The key observation is:

> All rotten oranges spread at the same time.

That means we do not perform BFS from one source and then another.  
We place **all initially rotten oranges into the BFS queue at the beginning**.

---

# 3. Example

```python
grid = [
    [2, 1, 1],
    [1, 1, 0],
    [0, 1, 1]
]
```

Initial state:

```text
2 1 1
1 1 0
0 1 1
```

After 1 minute:

```text
2 2 1
2 1 0
0 1 1
```

After 2 minutes:

```text
2 2 2
2 2 0
0 1 1
```

After 3 minutes:

```text
2 2 2
2 2 0
0 2 1
```

After 4 minutes:

```text
2 2 2
2 2 0
0 2 2
```

Therefore:

```text
Answer = 4
```

---

# 4. Graph Interpretation

Although the input is a matrix, this is fundamentally a graph problem.

Each usable grid cell can be considered a graph node.

Each cell may have edges to as many as four neighboring cells:

```text
        up
         |
left -- cell -- right
         |
        down
```

Rot spreads through these graph edges.

Because each move from one cell to another takes exactly one minute, every graph edge effectively has the same cost.

This is exactly the type of situation where **Breadth-First Search** is appropriate.

---

# 5. Why BFS Instead of DFS?

BFS explores nodes level by level.

Suppose a graph looks like:

```text
        A
      /   \
     B     C
    / \     \
   D   E     F
```

Starting from `A`, BFS visits:

```text
Level 0: A
Level 1: B, C
Level 2: D, E, F
```

For this problem:

```text
BFS level 0 = initially rotten oranges
BFS level 1 = oranges that rot after 1 minute
BFS level 2 = oranges that rot after 2 minutes
...
```

Therefore:

> One BFS level corresponds to one minute.

DFS, in contrast, follows one path deeply before exploring alternatives.  
That makes it poorly suited for directly modeling simultaneous minimum-time propagation.

---

# 6. Why Multi-Source BFS?

Consider:

```text
2 1 1 1 2
```

Both rotten oranges spread simultaneously.

At minute 1:

```text
2 2 1 2 2
```

At minute 2:

```text
2 2 2 2 2
```

The answer is `2`.

If we started BFS from only one rotten orange, we would fail to model simultaneous spread correctly.

Therefore, all rotten oranges are added to the queue before BFS begins.

```python
if grid[row][col] == 2:
    queue.append((row, col))
```

This converts ordinary BFS into **multi-source BFS**.

---

# 7. Core Strategy

We keep track of two things:

## 7.1 Queue of rotten oranges

```python
queue = deque()
```

Every initially rotten orange is inserted into the queue.

## 7.2 Number of fresh oranges

```python
fresh = 0
```

Every fresh orange increments this count.

Whenever a fresh orange becomes rotten:

```python
fresh -= 1
```

At the end:

- if `fresh == 0`, all oranges were reached
- if `fresh > 0`, some fresh oranges were unreachable

---

# 8. Optimal Solution

```python
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])

        queue = deque()
        fresh = 0

        # Step 1: Find all initially rotten oranges
        # and count all fresh oranges.
        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == 2:
                    queue.append((row, col))

                elif grid[row][col] == 1:
                    fresh += 1

        directions = [
            (1, 0),   # down
            (-1, 0),  # up
            (0, 1),   # right
            (0, -1)   # left
        ]

        minute = 0

        # Step 2: Multi-source BFS.
        while queue and fresh > 0:

            level_size = len(queue)

            # Process all oranges that are rotten
            # at the beginning of this minute.
            for _ in range(level_size):

                row, col = queue.popleft()

                for dr, dc in directions:

                    nr = row + dr
                    nc = col + dc

                    # Neighbor must be inside the grid
                    # and must contain a fresh orange.
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == 1
                    ):
                        # Mark immediately to avoid duplicate enqueueing.
                        grid[nr][nc] = 2

                        fresh -= 1

                        queue.append((nr, nc))

            minute += 1

        # Fresh oranges remain -> at least one was unreachable.
        if fresh > 0:
            return -1

        return minute
```

---

# 10. Step-by-Step Algorithm

## Step 1: Scan the grid

For every cell:

- rotten orange → add it to the queue
- fresh orange → increment `fresh`

Example:

```text
2 1 1
1 1 0
0 1 1
```

After scanning:

```text
queue = [(0, 0)]
fresh = 6
```

---

## Step 2: Start BFS

At each minute:

1. Record the number of currently rotten oranges in the queue.
2. Process exactly those oranges.
3. Rot every fresh neighboring orange.
4. Add newly rotten oranges to the queue.
5. Increment the minute count.

Why do we save:

```python
level_size = len(queue)
```

before the loop?

Because oranges added during the current minute should spread only during the **next minute**.

---

# 11. Why Mark a Fresh Orange Rotten Immediately?

When we discover:

```python
grid[nr][nc] == 1
```

we immediately execute:

```python
grid[nr][nc] = 2
```

before enqueueing.

This is equivalent to marking the node as visited.

Suppose:

```text
2 1 2
```

The middle fresh orange can be discovered from both sides.

If it is not marked immediately, both rotten oranges may enqueue it.

Correct pattern:

```python
grid[nr][nc] = 2
queue.append((nr, nc))
```

General BFS rule:

> Mark visited when adding a node to the queue, not when removing it.

---

# 12. Detailed Dry Run

Input:

```python
grid = [
    [2, 1, 1],
    [1, 1, 0],
    [0, 1, 1]
]
```

Initial scan:

```text
queue = [(0, 0)]
fresh = 6
minute = 0
```

## Minute 1

Process:

```text
(0, 0)
```

It rots:

```text
(0, 1)
(1, 0)
```

Grid:

```text
2 2 1
2 1 0
0 1 1
```

Now:

```text
fresh = 4
minute = 1
```

---

## Minute 2

Queue contains:

```text
(0, 1)
(1, 0)
```

They rot:

```text
(0, 2)
(1, 1)
```

Grid:

```text
2 2 2
2 2 0
0 1 1
```

Now:

```text
fresh = 2
minute = 2
```

---

## Minute 3

`(1, 1)` rots:

```text
(2, 1)
```

Grid:

```text
2 2 2
2 2 0
0 2 1
```

Now:

```text
fresh = 1
minute = 3
```

---

## Minute 4

`(2, 1)` rots:

```text
(2, 2)
```

Grid:

```text
2 2 2
2 2 0
0 2 2
```

Now:

```text
fresh = 0
minute = 4
```

Answer:

```text
4
```

---

# 13. Pseudocode

```text
FUNCTION orangesRotting(grid):

    rows = number of rows
    cols = number of columns

    queue = empty queue
    fresh = 0

    FOR each row:
        FOR each column:

            IF cell is rotten:
                add cell to queue

            ELSE IF cell is fresh:
                fresh += 1

    directions = up, down, left, right

    minutes = 0

    WHILE queue is not empty AND fresh > 0:

        level_size = size of queue

        REPEAT level_size times:

            remove one rotten orange

            FOR each of four directions:

                compute neighboring row and column

                IF neighbor is inside grid
                   AND neighbor is fresh:

                    mark neighbor rotten
                    fresh -= 1
                    add neighbor to queue

        minutes += 1

    IF fresh > 0:
        RETURN -1

    RETURN minutes
```

---

# 14. Correctness Intuition

BFS guarantees that cells are processed in increasing order of their shortest distance from the source.

Because all initially rotten oranges are inserted into the queue at time `0`, this becomes a multi-source shortest-path search.

A fresh orange that is one edge away from any rotten orange is processed after one BFS level.

A fresh orange two edges away is processed after two levels.

And so on.

Therefore the first time a fresh orange becomes rotten is exactly the earliest possible minute at which rot can reach it.

The total answer is the largest such minimum distance among all reachable fresh oranges.

If a fresh orange is unreachable, it remains fresh after BFS terminates and we return `-1`.

---

# 15. More Formal Correctness Argument

We can state an invariant:

> At the beginning of BFS minute `t`, every orange currently in the queue became rotten at exactly minute `t`.

### Base case

Initially, the queue contains all oranges already rotten at minute `0`.

So the invariant holds for `t = 0`.

### Inductive step

Assume every orange currently being processed became rotten at minute `t`.

Each fresh neighbor of those oranges can therefore become rotten at minute `t + 1`.

Those neighbors are inserted into the queue for the next BFS level.

Because BFS processes all distance-`t` nodes before any distance-`t+1` nodes, no orange that can rot earlier is delayed.

Thus, the invariant holds for minute `t + 1`.

Therefore BFS computes the minimum rotting time for every reachable fresh orange.

---

# 16. Complexity Analysis

Let:

```text
m = number of rows
n = number of columns
```

## Time complexity

Initial grid scan:

```text
O(mn)
```

During BFS, each fresh orange is converted to rotten at most once and inserted into the queue at most once.

Each cell checks at most four neighbors.

Therefore:

```text
O(mn)
```

Overall:

```text
O(mn)
```

## Space complexity

In the worst case, the queue may contain `O(mn)` cells.

Therefore:

```text
O(mn)
```

No separate visited matrix is required because changing:

```python
1 -> 2
```

also marks that cell visited.

---

# 17. Multiple Test Cases

## Test Case 1 — Standard Example

```python
grid = [
    [2, 1, 1],
    [1, 1, 0],
    [0, 1, 1]
]
```

Expected:

```text
4
```

---

## Test Case 2 — Unreachable Fresh Orange

```python
grid = [
    [2, 1, 1],
    [0, 1, 1],
    [1, 0, 1]
]
```

Expected:

```text
-1
```

Reason:

The fresh orange at `(2, 0)` cannot be reached.

---

## Test Case 3 — No Fresh Oranges

```python
grid = [
    [0, 2]
]
```

Expected:

```text
0
```

---

## Test Case 4 — No Rotten Orange Exists

```python
grid = [
    [1, 1],
    [1, 1]
]
```

Expected:

```text
-1
```

---

## Test Case 5 — Single Rotten Orange

```python
grid = [[2]]
```

Expected:

```text
0
```

---

## Test Case 6 — Single Fresh Orange

```python
grid = [[1]]
```

Expected:

```text
-1
```

---

## Test Case 7 — Multiple Sources

```python
grid = [[2, 1, 1, 1, 2]]
```

Expected:

```text
2
```

---

## Test Case 8 — Rectangular Grid

```python
grid = [
    [2, 1, 1, 1]
]
```

Expected:

```text
3
```

This test is particularly useful for detecting row/column boundary bugs.

---

## Test Case 9 — Empty Cells Separate Regions

```python
grid = [
    [2, 0, 1],
    [0, 0, 0],
    [1, 0, 2]
]
```

Expected:

```text
-1
```

Both isolated fresh oranges are unreachable.

---

## Test Case 10 — All Rotten

```python
grid = [
    [2, 2],
    [2, 2]
]
```

Expected:

```text
0
```

---

# 18. Hard-Coded Local Testing Version

```python
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])

        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == 2:
                    queue.append((row, col))

                elif grid[row][col] == 1:
                    fresh += 1

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        minute = 0

        while queue and fresh > 0:

            for _ in range(len(queue)):

                row, col = queue.popleft()

                for dr, dc in directions:

                    nr = row + dr
                    nc = col + dc

                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == 1
                    ):
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))

            minute += 1

        return minute if fresh == 0 else -1


tests = [
    (
        [
            [2, 1, 1],
            [1, 1, 0],
            [0, 1, 1]
        ],
        4
    ),
    (
        [
            [2, 1, 1],
            [0, 1, 1],
            [1, 0, 1]
        ],
        -1
    ),
    (
        [[0, 2]],
        0
    ),
    (
        [[1]],
        -1
    ),
    (
        [[2]],
        0
    ),
    (
        [[2, 1, 1, 1, 2]],
        2
    )
]


for i, (grid, expected) in enumerate(tests, start=1):

    result = Solution().orangesRotting(grid)

    print(
        f"Test {i}: "
        f"result={result}, "
        f"expected={expected}, "
        f"passed={result == expected}"
    )
```

---

# 19. Python Implementation Guidance

## 19.1 Use `deque`

Import:

```python
from collections import deque
```

Use:

```python
queue.popleft()
```

instead of:

```python
list.pop(0)
```

`deque.popleft()` is `O(1)`.

Removing index `0` from a Python list is `O(n)` because remaining elements must be shifted.

---

## 19.2 Use direction vectors

Instead of repeating four separate condition blocks:

```python
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]
```

Then:

```python
for dr, dc in directions:
    nr = row + dr
    nc = col + dc
```

This technique is reusable in almost every matrix traversal problem.

---

## 19.3 Modify the grid in place

Instead of using:

```python
visited = set()
```

or:

```python
visited = [[False] * cols for _ in range(rows)]
```

we can use the grid itself:

```python
grid[nr][nc] = 2
```

This simultaneously means:

- the orange is now rotten
- the cell has been visited
- do not enqueue it again

---

## 19.4 Use `if / elif`

Since a cell cannot be both fresh and rotten, this is semantically clean:

```python
if grid[row][col] == 2:
    ...
elif grid[row][col] == 1:
    ...
```

Two independent `if` statements are also logically correct here because the values are mutually exclusive, but `if/elif` expresses intent better.

---

# 20. Common Mistakes

## Mistake 1 — Using DFS for minimum-time propagation

DFS does not naturally process cells in shortest-distance order.

Use BFS.

---

## Mistake 2 — Starting from only one rotten orange

All rotten oranges act simultaneously.

Use multi-source BFS.

---

## Mistake 3 — Incrementing time once per node

Wrong:

```python
while queue:
    row, col = queue.popleft()
    minute += 1
```

Minutes correspond to BFS levels, not individual nodes.

---

## Mistake 4 — Marking visited too late

Prefer:

```python
grid[nr][nc] = 2
queue.append((nr, nc))
```

Do not wait until dequeue time to mark it.

---

## Mistake 5 — Using `rows` for column bounds

Wrong:

```python
0 <= nc < rows
```

Correct:

```python
0 <= nc < cols
```

---

## Mistake 6 — Forgetting unreachable oranges

After BFS:

```python
if fresh > 0:
    return -1
```

---

## Mistake 7 — Off-by-one minute counting

A clean structure is:

```python
while queue and fresh > 0:

    for _ in range(len(queue)):
        ...

    minute += 1
```

This avoids counting unnecessary levels after all fresh oranges have already rotted.

---

# 21. Alternative BFS Design — Store Time in the Queue

Instead of processing levels explicitly, each queue item can contain time:

```python
(row, col, time)
```

Example:

```python
queue.append((row, col, 0))
```

Then:

```python
row, col, time = queue.popleft()
```

A new orange receives:

```python
queue.append((nr, nc, time + 1))
```

Example implementation:

```python
from collections import deque


class Solution:
    def orangesRotting(self, grid):

        rows = len(grid)
        cols = len(grid[0])

        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == 2:
                    queue.append((row, col, 0))

                elif grid[row][col] == 1:
                    fresh += 1

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        answer = 0

        while queue:

            row, col, time = queue.popleft()

            answer = max(answer, time)

            for dr, dc in directions:

                nr = row + dr
                nc = col + dc

                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == 1
                ):
                    grid[nr][nc] = 2
                    fresh -= 1

                    queue.append((nr, nc, time + 1))

        return answer if fresh == 0 else -1
```

Both implementations are correct.

The level-by-level version is usually easier to explain in interviews because:

```text
one BFS level = one minute
```

is explicit.

---

# 22. Interview Questions and Answers

This section is intentionally detailed because Rotting Oranges is often used to test whether a candidate truly understands BFS rather than merely memorizing a template.

---

# Easy Interview Questions

## Q1. What algorithmic pattern does Rotting Oranges use?

**Answer:**

The optimal solution uses **multi-source breadth-first search**.

It is BFS because the problem asks for minimum time in a graph where each move from one cell to an adjacent cell has equal cost.

It is multi-source because multiple oranges may initially be rotten, and all of them begin spreading simultaneously.

Instead of running independent BFS traversals, all initially rotten oranges are inserted into the queue before traversal begins.

This creates a single BFS wave expanding from all sources simultaneously.

---

## Q2. Why is BFS appropriate for minimum time?

**Answer:**

BFS explores an unweighted graph in increasing order of shortest-path distance from the source.

Every transition from one cell to an adjacent cell represents exactly one minute.

Therefore:

```text
distance 0 -> minute 0
distance 1 -> minute 1
distance 2 -> minute 2
```

Because all edges have equal cost, BFS guarantees that the first time a fresh orange is reached is the earliest possible time it could become rotten.

---

## Q3. Why is this called multi-source BFS?

**Answer:**

Ordinary BFS begins from one starting node.

Multi-source BFS begins with several source nodes already inside the queue.

For Rotting Oranges, every initially rotten orange is a source.

```python
if grid[row][col] == 2:
    queue.append((row, col))
```

All those cells are considered distance `0`.

BFS then computes distance to the nearest source for every reachable fresh orange.

---

## Q4. Why do we count fresh oranges?

**Answer:**

The fresh count allows us to efficiently determine whether every fresh orange was eventually reached.

Whenever one becomes rotten:

```python
fresh -= 1
```

At the end:

```python
if fresh == 0:
    return minutes
else:
    return -1
```

Without this count, we would need another complete grid scan after BFS.

The fresh counter also allows early termination once all oranges become rotten.

---

## Q5. Why do we mark an orange rotten before adding it to the queue?

**Answer:**

This prevents the same fresh orange from being discovered multiple times.

Suppose two rotten oranges are both adjacent to one fresh orange.

If we enqueue the fresh orange without immediately marking it, the second rotten orange may also enqueue it.

By changing:

```python
grid[nr][nc] = 2
```

before enqueueing, we ensure that any later neighbor sees the cell as already processed.

This follows the general BFS principle:

> Mark a node visited when it is enqueued.

---

## Q6. What does one BFS level represent?

**Answer:**

One BFS level represents one minute.

Every orange in the queue at the beginning of a level is already rotten at the same time step.

All fresh neighbors reached from that level become rotten simultaneously and are processed in the following level.

---

## Q7. Why do we use `deque` instead of a list?

**Answer:**

A BFS queue repeatedly removes elements from the front.

With:

```python
deque.popleft()
```

removal is `O(1)`.

With:

```python
list.pop(0)
```

removal is `O(n)` because all remaining elements must shift left.

Using a list could therefore make a BFS implementation unnecessarily inefficient.

---

## Q8. What are the four direction vectors?

**Answer:**

```python
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]
```

These represent:

```text
down
up
right
left
```

For each current cell:

```python
nr = row + dr
nc = col + dc
```

produces the neighboring coordinates.

---

## Q9. Why don't diagonal oranges become rotten?

**Answer:**

Because the problem defines adjacency using only four-directional neighbors.

A diagonal position changes both row and column simultaneously, for example:

```text
(row + 1, col + 1)
```

Such moves are not included in the direction array.

---

## Q10. What is the time complexity?

**Answer:**

`O(mn)`.

We first scan all `m * n` cells.

During BFS, every fresh orange is enqueued at most once.

Each dequeued cell checks at most four neighbors, which is a constant amount of work.

Therefore total complexity remains:

```text
O(mn)
```

---

# Medium Interview Questions

## Q11. Why not run BFS separately from every rotten orange?

**Answer:**

Suppose there are `k` rotten oranges.

Running BFS independently from each one could require roughly:

```text
O(kmn)
```

work in the worst case.

It also complicates the simultaneous-time interpretation.

Multi-source BFS initializes the queue with all rotten oranges and performs only one traversal:

```text
O(mn)
```

Conceptually, multi-source BFS behaves as though we created a virtual super-source connected to every initially rotten orange with zero-cost edges.

---

## Q12. What shortest-path quantity is this algorithm computing?

**Answer:**

For each reachable fresh orange, BFS computes:

```text
minimum Manhattan-step distance
to any initially rotten orange
subject to obstacles
```

The answer is the maximum of these minimum distances.

In mathematical terms, if `S` is the set of initially rotten oranges, then for every reachable fresh cell `v`, the rotting time is:

```text
min distance(s, v) over all s in S
```

The final answer is:

```text
max over all fresh cells of their minimum source distance
```

provided every fresh cell is reachable.

---

## Q13. Why doesn't a normal grid scan correctly simulate time?

**Answer:**

If we mutate the grid while scanning it, a newly rotten orange could immediately infect another orange during the same scan.

For:

```text
2 1 1 1
```

a naive left-to-right scan could accidentally produce:

```text
2 2 2 2
```

in one iteration.

But physically the spread requires three minutes.

BFS avoids this because newly rotten oranges are saved for the next level.

---

## Q14. Could DFS be modified to solve the problem correctly?

**Answer:**

Yes, but it would be more complicated.

One possibility is to perform DFS while tracking arrival times and repeatedly update cells whenever a shorter time is found.

However, this essentially recreates shortest-path relaxation.

Because every edge has equal weight, BFS directly provides shortest distances with simpler logic and better guarantees.

The question is not whether DFS can somehow be made to work, but which algorithm naturally matches the mathematical structure.

That is BFS.

---

## Q15. Why does the algorithm stop when `fresh == 0`?

**Answer:**

Once there are no fresh oranges left, the requested condition has already been satisfied.

There may still be rotten cells in the queue, but processing them cannot improve the answer because there is nothing left to infect.

Therefore:

```python
while queue and fresh > 0:
```

avoids unnecessary BFS levels and simplifies minute counting.

---

## Q16. What happens if the grid contains no fresh oranges initially?

**Answer:**

`fresh` is initialized to `0` and remains `0`.

The BFS loop:

```python
while queue and fresh > 0:
```

does not execute.

The algorithm returns:

```text
0
```

This is correct because zero minutes are required.

---

## Q17. What happens if fresh oranges exist but no rotten oranges exist?

**Answer:**

The queue is empty while:

```text
fresh > 0
```

Therefore BFS never starts.

At the end, fresh oranges remain, so the algorithm returns:

```text
-1
```

This is correct because there is no infection source.

---

## Q18. Why can the grid itself act as the visited structure?

**Answer:**

Before visiting a fresh cell it contains:

```text
1
```

When it is discovered, we set:

```text
2
```

From that point onward, it will fail the condition:

```python
grid[nr][nc] == 1
```

Thus it cannot be rediscovered.

That means the grid state itself records visitation.

A separate `visited` set or matrix would be redundant.

---

## Q19. What if modifying the input is not allowed?

**Answer:**

Then we should preserve the original grid and maintain a separate visited structure.

For example:

```python
visited = [[False] * cols for _ in range(rows)]
```

When a fresh orange is discovered:

```python
visited[nr][nc] = True
queue.append((nr, nc))
```

Alternatively, copy the grid first:

```python
copy_grid = [row[:] for row in grid]
```

The algorithmic complexity remains `O(mn)` space either way.

---

## Q20. Why is `level_size = len(queue)` necessary?

**Answer:**

The queue changes while we process it.

Newly rotten oranges are appended to the back.

If we simply continued until the queue became empty, we would mix multiple time steps together.

Capturing:

```python
level_size = len(queue)
```

means:

> Process only the oranges that were already rotten at the beginning of this minute.

The newly appended cells remain for the next minute.

---

# Difficult Interview Questions

## Q21. Can you prove that each orange is assigned the minimum possible rotting time?

**Answer:**

Yes.

Consider the graph whose vertices are non-empty cells and whose edges connect orthogonally adjacent cells.

Every edge has weight `1`.

All initially rotten oranges are sources with distance `0`.

Multi-source BFS is equivalent to running BFS from an artificial super-source connected to all initial rotten oranges by zero-cost conceptual edges.

For any fresh orange `v`, BFS processes graph vertices in nondecreasing shortest-path distance.

Therefore the first time `v` is discovered corresponds to:

```text
min shortest_path(source, v)
```

over every initial rotten source.

Any hypothetical earlier rotting time would imply a shorter path than the one BFS found, contradicting the BFS shortest-path property.

---

## Q22. How would the solution change if infection times differed between cells?

**Answer:**

Ordinary BFS works because every transition costs exactly one minute.

If transition costs differ, then BFS is no longer generally correct.

For nonnegative variable costs, the natural algorithm becomes **Dijkstra's algorithm**.

Example:

Suppose entering each cell costs:

```text
1, 3, 7, ...
```

Then the queue must become a priority queue:

```python
heapq
```

and nodes should be processed in increasing accumulated infection time.

This is an important generalization:

```text
equal edge cost -> BFS
0/1 edge cost -> 0-1 BFS
arbitrary nonnegative edge cost -> Dijkstra
negative edge cost -> different shortest-path methods
```

---

## Q23. What if some oranges take two minutes to infect neighboring oranges?

**Answer:**

Then the graph has weighted edges.

If each source/orange has a different infection delay, we cannot simply map one BFS layer to one minute.

We would instead represent the next infection event with an accumulated timestamp and use a min-heap.

The state could be:

```python
(time, row, col)
```

The next cell to process would always be the one with the smallest infection time.

That converts the problem into a multi-source Dijkstra problem.

---

## Q24. How could you solve the problem without explicitly processing BFS levels?

**Answer:**

Store time inside each queue element:

```python
(row, col, time)
```

Initially:

```python
queue.append((row, col, 0))
```

A fresh neighbor receives:

```python
queue.append((nr, nc, time + 1))
```

The maximum discovered time becomes the answer.

This removes the outer level-size structure while preserving BFS behavior.

---

## Q25. Can the answer be viewed as a distance transform?

**Answer:**

Yes.

The algorithm effectively computes a discrete distance transform over the traversable portion of the grid.

Every initially rotten orange has distance `0`.

Each reachable fresh orange receives the shortest graph distance to the nearest rotten source.

The final answer is the maximum finite distance assigned to an initially fresh cell.

This interpretation connects the problem to:

- image processing
- wave-front propagation
- nearest-source maps
- Voronoi-like grid partitioning
- geodesic distance computation

---

## Q26. How would you also return the minute at which every individual orange rots?

**Answer:**

Maintain a separate time matrix:

```python
time = [[-1] * cols for _ in range(rows)]
```

Initialize rotten oranges with:

```python
time[row][col] = 0
```

When a fresh neighbor is discovered:

```python
time[nr][nc] = time[row][col] + 1
```

At the end, the matrix stores each orange's infection time.

Unreachable fresh oranges remain `-1`.

---

## Q27. How would you return which original rotten orange infected each cell?

**Answer:**

Associate each initial source with a source identifier.

Queue items could contain:

```python
(row, col, source_id)
```

When infection spreads:

```python
owner[nr][nc] = source_id
```

This partitions the reachable grid according to the source that reaches each cell first.

It is similar to constructing a multi-source BFS Voronoi diagram.

Tie behavior would need to be explicitly defined.

---

## Q28. What if diagonal spreading were also allowed?

**Answer:**

Add four diagonal directions:

```python
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]
```

The BFS framework remains unchanged.

Only graph connectivity changes.

---

## Q29. What if the grid wraps around like a torus?

**Answer:**

Neighbor coordinates can be wrapped using modulo:

```python
nr = (row + dr) % rows
nc = (col + dc) % cols
```

Then moving beyond one boundary enters from the opposite side.

Again, the BFS framework remains unchanged because every transition still has equal cost.

---

## Q30. What if walls can disappear after a certain time?

**Answer:**

Then the state is no longer determined solely by `(row, col)`.

Time becomes part of the state because whether a move is valid may depend on when the cell is reached.

A state might become:

```text
(row, col, time)
```

or some compressed time-state representation.

This illustrates a critical interview concept:

> If future legal moves depend on additional information, that information may need to be included in the graph state.

---

## Q31. Could this be parallelized?

**Answer:**

Conceptually yes, because all nodes in one BFS frontier can be processed independently.

However, implementation requires synchronization when multiple frontier cells attempt to infect the same fresh orange.

A shared atomic visited/rotted state or frontier deduplication would be required.

The level-synchronous nature of BFS maps naturally to parallel graph processing systems.

---

## Q32. How would you generalize this to a three-dimensional grid?

**Answer:**

A cell would have up to six orthogonal neighbors:

```text
x + 1
x - 1
y + 1
y - 1
z + 1
z - 1
```

Queue states would become:

```python
(x, y, z)
```

The same multi-source BFS logic still applies.

Complexity becomes proportional to the number of volume cells:

```text
O(XYZ)
```

---

## Q33. Can we avoid storing all rotten oranges in the queue initially?

**Answer:**

Not if we want a clean multi-source BFS using the queue structure.

We need all initial sources to participate at distance zero.

One could construct an equivalent artificial source connected to all rotten cells, but discovering those connections still requires identifying the initial rotten cells.

So practically, scanning and enqueueing all initial sources is the natural solution.

---

## Q34. What is the precise relationship between Rotting Oranges and shortest path?

**Answer:**

Let the graph contain every non-empty grid cell.

Add an edge of weight `1` between orthogonally adjacent non-empty cells.

Let `S` be the set of initially rotten oranges.

For every initially fresh orange `v`, define:

```text
d(v) = min distance(s, v), for s in S
```

If no source can reach `v`, then:

```text
d(v) = infinity
```

The problem asks for:

```text
max d(v)
```

over all initially fresh oranges, unless any distance is infinite, in which case the answer is `-1`.

Multi-source BFS computes all these distances in linear time.

---

## Q35. Why is the result not simply the number of BFS iterations until the queue is empty?

**Answer:**

Because after the final fresh orange becomes rotten, it may still remain in the queue.

If we continue counting until the queue is empty, we may count an extra level in implementations that increment time unconditionally.

Using:

```python
while queue and fresh > 0:
```

ensures that time stops when the required condition is reached.

Another valid strategy is to initialize time differently or subtract one at the end, but that is easier to get wrong.

---

# 23. Interview Follow-Up Variants

An interviewer may modify the problem.

You should be ready for variants such as:

### Variant A — Return infection time for every orange

Use a distance matrix.

### Variant B — Infection spreads diagonally

Use eight directions.

### Variant C — Different spread costs

Use Dijkstra.

### Variant D — Some cells are immune

Treat them as obstacles.

### Variant E — Return the source responsible for each infection

Propagate source IDs through multi-source BFS.

### Variant F — Multiple infection types

State may need to include infection type, and conflict-resolution rules must be defined.

### Variant G — Infection spreads only during selected time windows

Time becomes part of the state.

---

# 24. Similar LeetCode Problems

## LeetCode 286 — Walls and Gates

Pattern:

```text
Multi-source BFS
```

All gates are sources.

Compute the shortest distance from each room to its nearest gate.

This is one of the closest conceptual relatives to Rotting Oranges.

---

## LeetCode 542 — 01 Matrix

Pattern:

```text
Multi-source BFS
```

All zero-valued cells are inserted into the queue initially.

For each `1`, determine the distance to the nearest `0`.

---

## LeetCode 1162 — As Far from Land as Possible

Pattern:

```text
Multi-source BFS
```

All land cells are sources.

Expand into water and find the water cell farthest from land.

---

## LeetCode 1091 — Shortest Path in Binary Matrix

Pattern:

```text
Single-source BFS
```

Find shortest path in an unweighted grid.

Unlike Rotting Oranges, diagonal movement is allowed.

---

## LeetCode 1926 — Nearest Exit from Entrance in Maze

Pattern:

```text
Single-source BFS
```

Find the closest boundary exit.

---

## LeetCode 200 — Number of Islands

Pattern:

```text
DFS/BFS connected components
```

This problem asks how many disconnected land components exist rather than shortest distance.

---

## LeetCode 695 — Max Area of Island

Pattern:

```text
DFS/BFS connected component size
```

Explore each island and compute its area.

---

## LeetCode 733 — Flood Fill

Pattern:

```text
DFS/BFS grid traversal
```

Change all connected cells of the same original color.

---

## LeetCode 994 — Rotting Oranges

Pattern:

```text
Multi-source BFS with time
```

The current problem.

---

## LeetCode 317 — Shortest Distance from All Buildings

More difficult.

Requires combining distances from multiple buildings, but unlike ordinary multi-source BFS, the objective is total distance to **all** buildings rather than minimum distance to any one source.

---

## LeetCode 934 — Shortest Bridge

Uses DFS/BFS combination.

First identify one island, then use BFS expansion to reach the second island.

---

## LeetCode 1293 — Shortest Path in a Grid with Obstacles Elimination

Advanced BFS.

State includes:

```text
(row, col, obstacles_remaining)
```

This demonstrates how BFS state grows when future possibilities depend on additional information.

---

# 25. Similar Non-LeetCode Exercises

## Exercise 1 — Fire Spread in a Forest

A forest is represented by:

```text
0 = empty
1 = tree
2 = burning tree
```

Every minute, burning trees ignite adjacent trees.

Return the number of minutes required to burn every reachable tree.

If some tree can never burn, return `-1`.

### Test

```python
forest = [
    [2, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]
```

Expected:

```text
4
```

Hint:

This is almost identical to Rotting Oranges.

---

## Exercise 2 — Virus Spread

A laboratory grid contains:

```text
0 = wall
1 = uninfected cell
2 = infected cell
```

Infection spreads to four-directional adjacent cells every second.

Find the time to infect all reachable cells.

### Test

```python
lab = [
    [2, 1, 1, 0],
    [1, 1, 1, 1],
    [0, 1, 2, 1]
]
```

Work out the answer manually before coding.

---

## Exercise 3 — Nearest Hospital

Given a city grid:

```text
0 = road
1 = building
2 = hospital
```

For each road cell, return its minimum distance to a hospital.

### Test

```python
city = [
    [2, 0, 0],
    [0, 0, 0],
    [0, 0, 2]
]
```

Expected distance matrix for traversable cells should reflect distance to the closest hospital.

Hint:

Start BFS from both hospitals simultaneously.

---

## Exercise 4 — Flood from Multiple Rivers

Grid:

```text
0 = dry land
1 = river
-1 = wall
```

Each minute, water spreads from river cells into neighboring dry cells.

Return the earliest flooding time for every dry cell.

### Test

```python
grid = [
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
]
```

Instead of returning one number, return a time matrix.

---

## Exercise 5 — Chemical Contamination

Multiple chemical leaks begin at several cells.

Every move takes one second.

Some cells are walls.

Determine:

1. when every reachable cell becomes contaminated
2. which source reaches each cell first

### Test

```python
grid = [
    [2, 1, 1, 1, 2],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1]
]
```

This exercise adds source tracking.

---

## Exercise 6 — Weighted Infection

Each cell contains the number of minutes required for infection to pass through it.

Example:

```python
cost = [
    [0, 1, 4],
    [2, 3, 1],
    [1, 1, 1]
]
```

Starting from `(0, 0)`, compute the earliest infection time for every cell.

This is **not ordinary BFS**.

Hint:

Use Dijkstra's algorithm.

---

# 26. Practice Questions Without Solutions

## Easy

1. Modify the solution so diagonal neighbors are also infected.
2. Return the total number of oranges that became rotten.
3. Return `True/False` depending on whether all oranges can eventually rot.
4. Count how many oranges rot at each minute.
5. Return the coordinates of unreachable fresh oranges.

## Medium

1. Return an infection-time matrix.
2. Return the original source responsible for each infected orange.
3. Support cells that become passable only after a certain minute.
4. Support multiple infection types with priority rules.
5. Compute how many cells each initial source infects.

## Hard

1. Allow variable transmission costs between cells.
2. Allow the environment to change over time.
3. Model infection spreading in a 3D lattice.
4. Support portals that teleport infection with zero cost.
5. Find the minimum number of initial rotten oranges needed to infect all reachable oranges within `T` minutes.

---

# 27. Concept Recognition Checklist

When reading a new problem, ask:

### Does something spread?

Examples:

```text
fire
water
infection
signal
distance
contamination
```

### Is movement local?

For example:

```text
up/down/left/right
```

### Does every move cost the same?

If yes, BFS is promising.

### Are there multiple starting points?

If yes:

```text
multi-source BFS
```

### Is the question about minimum time or minimum steps?

Again:

```text
BFS
```

This recognition pattern is more valuable than memorizing the exact Rotting Oranges implementation.

---

# 28. Mental Template for Multi-Source BFS

Memorize the structure, not the exact variable names:

```python
queue = deque()

for every cell:
    if source:
        queue.append(cell)

while queue:

    for _ in range(len(queue)):

        current = queue.popleft()

        for neighbor in neighbors(current):

            if valid and unvisited:

                mark visited

                queue.append(neighbor)
```

The pattern appears repeatedly in interviews.

---

# 29. Comparison: BFS vs DFS vs Dijkstra

| Situation | Best candidate |
|---|---|
| Explore connected component | DFS or BFS |
| Minimum steps with equal edge costs | BFS |
| Multiple equal-cost sources | Multi-source BFS |
| Edges cost only 0 or 1 | 0-1 BFS |
| Nonnegative arbitrary edge costs | Dijkstra |
| Topological dependency graph | Topological sort |
| Need every possible path | Backtracking / DFS |

For Rotting Oranges:

```text
equal edge cost = 1 minute
multiple sources
minimum propagation time
```

Therefore:

```text
Multi-source BFS
```

---

# 30. Final Interview-Ready Explanation

A strong answer in a technical interview could be:

> I model the grid as an unweighted graph. Each non-empty cell is a node, and orthogonally adjacent cells are connected. Because all initially rotten oranges begin spreading simultaneously, I use multi-source BFS by inserting every rotten orange into the queue before traversal starts. I also count the number of fresh oranges.
>
> Each BFS level corresponds to one minute. While processing a level, I inspect the four neighbors of every currently rotten orange. If a neighbor is fresh, I immediately mark it rotten, decrement the fresh count, and enqueue it for the next BFS level. Marking it before enqueueing prevents duplicate processing.
>
> BFS guarantees minimum propagation time because every move has equal cost. If fresh oranges remain after the queue is exhausted, they are unreachable and I return `-1`. Otherwise I return the number of BFS levels required.
>
> The time complexity is `O(mn)` because each cell is processed at most once, and the worst-case auxiliary space is `O(mn)` for the queue.

---

# 31. Key Takeaways

The most important ideas from this problem are:

1. A matrix can often be treated as a graph.
2. Minimum steps in an unweighted graph suggests BFS.
3. Simultaneous spreading from multiple locations suggests multi-source BFS.
4. BFS levels can directly represent elapsed time.
5. Mark nodes visited when enqueueing them.
6. Reuse grid state as visitation information when allowed.
7. Keep a count of remaining target nodes when it helps detect completion.
8. Use `deque` for efficient BFS in Python.
9. Carefully distinguish `rows` from `cols`.
10. Understand why an algorithm works instead of memorizing code.

The core mental shortcut is:

```text
Rotting Oranges
= grid
+ simultaneous spread
+ minimum time
= multi-source BFS
```
