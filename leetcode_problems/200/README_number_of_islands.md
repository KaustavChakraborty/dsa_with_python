# LeetCode 200 — Number of Islands

A detailed study guide for **LeetCode 200: Number of Islands**, focused on understanding the graph-traversal pattern behind the problem and preparing for technical interviews at product-based companies.

---

## 1. Problem Statement

You are given an `m x n` 2D binary grid where:

- `"1"` represents **land**
- `"0"` represents **water**

An island is formed by connecting adjacent land cells **horizontally or vertically**.

Diagonal cells are **not** connected.

Return the number of islands in the grid.

### Example

```text
Input:

[
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","1","1","1"]
]

Output:
2
```

Explanation:

```text
Island 1:
1 1
1 1

Island 2:
    1
    1 1 1
```

So the grid contains exactly `2` connected components of land.

---

# 2. Why This Is Really a Graph Problem

Although the input is a matrix, the cleanest mental model is an **implicit graph**.

Each land cell is a graph node.

Two land cells have an edge between them when they are adjacent in one of four directions:

```text
        up
         ↑
left ← cell → right
         ↓
        down
```

For a cell `(row, col)`, the four possible neighbors are:

```python
(row - 1, col)     # up
(row + 1, col)     # down
(row, col - 1)     # left
(row, col + 1)     # right
```

Therefore the problem becomes:

> Count the number of connected components among all land cells.

This connection is extremely important because the same idea appears in many graph and matrix interview problems.

---

# 3. Core Observation

Suppose we scan every cell in the matrix.

When we encounter an unvisited land cell:

```python
grid[row][col] == "1"
```

that cell must be the beginning of a **new island**.

So we increment the answer:

```python
island += 1
```

Then we run DFS or BFS from that cell and visit every land cell belonging to the same connected component.

After that traversal finishes, the entire island has been marked visited.

The algorithm therefore follows this general pattern:

```text
for every cell:
    if cell is unvisited land:
        number_of_islands += 1
        visit the entire connected component
```

This is the standard **connected-components traversal pattern**.

---

# 4. Solution Used in This Repository

The provided solution uses **recursive Depth-First Search (DFS)**.

The main idea is:

1. Scan the entire grid.
2. Whenever `"1"` is found:
   - increment the island count,
   - start DFS from that cell.
3. DFS changes every connected `"1"` into `"0"`.
4. Continue scanning.
5. Return the number of DFS launches.

The key insight is:

> The number of islands equals the number of times we have to start a new DFS from an unvisited land cell.

---

# 5. Reference Python Implementation

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        rows = len(grid)
        cols = len(grid[0])

        island = 0

        def dfs(row, col):

            if row < 0 or row >= rows or col < 0 or col >= cols:
                return

            if grid[row][col] == "0":
                return

            # Mark current land cell as visited
            grid[row][col] = "0"

            # Explore all four directions
            dfs(row + 1, col)
            dfs(row - 1, col)
            dfs(row, col + 1)
            dfs(row, col - 1)

        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == "1":
                    island += 1
                    dfs(row, col)

        return island
```

---

# 6. Step-by-Step Dry Run

Consider:

```text
[
  ["1","1","0","0"],
  ["1","0","0","1"],
  ["0","0","1","1"],
  ["0","0","0","0"]
]
```

Initial state:

```text
1 1 0 0
1 0 0 1
0 0 1 1
0 0 0 0
```

## Step 1

We scan from the top-left.

Cell `(0,0)` is `"1"`.

Therefore:

```text
island = 1
```

Start:

```python
dfs(0, 0)
```

DFS visits:

```text
(0,0)
(0,1)
(1,0)
```

Those cells are changed to `"0"`.

Grid becomes:

```text
0 0 0 0
0 0 0 1
0 0 1 1
0 0 0 0
```

## Step 2

Continue scanning.

Cell `(1,3)` is `"1"`.

Therefore:

```text
island = 2
```

DFS visits:

```text
(1,3)
(2,3)
(2,2)
```

Grid becomes:

```text
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```

Final answer:

```text
2
```

---

# 7. Why Changing `"1"` to `"0"` Works

Normally DFS/BFS problems use a separate data structure such as:

```python
visited = set()
```

This solution instead modifies the grid:

```python
grid[row][col] = "0"
```

This has the same logical meaning as:

```text
This cell has already been visited.
```

The transformation is therefore:

```text
unvisited land  ->  visited land
"1"             ->  "0"
```

This avoids allocating an additional visited matrix or hash set.

---

# 8. Why Increment Before DFS?

The code does:

```python
if grid[row][col] == "1":
    island += 1
    dfs(row, col)
```

Why is every encountered `"1"` guaranteed to represent a new island?

Because if it belonged to an island that had already been discovered, the previous DFS would already have changed it to `"0"`.

Therefore any `"1"` remaining during the outer scan has not yet been visited and must belong to a new connected component.

---

# 9. Base Cases in DFS

The DFS must stop in two situations.

## Case 1: Outside the Grid

```python
if row < 0 or row >= rows or col < 0 or col >= cols:
    return
```

Without this condition, accessing:

```python
grid[row][col]
```

could result in invalid indexing.

## Case 2: Water or Already Visited Cell

```python
if grid[row][col] == "0":
    return
```

Since visited land is also converted to `"0"`, this condition handles both:

- actual water,
- previously visited land.

---

# 10. Pseudocode

```text
FUNCTION numberOfIslands(grid):

    rows = number of rows
    cols = number of columns

    islandCount = 0

    DEFINE DFS(row, col):

        IF row or col is outside grid:
            RETURN

        IF grid[row][col] is water:
            RETURN

        mark grid[row][col] as visited

        DFS(row + 1, col)
        DFS(row - 1, col)
        DFS(row, col + 1)
        DFS(row, col - 1)

    FOR each row:
        FOR each column:

            IF current cell is unvisited land:
                islandCount += 1
                DFS(current cell)

    RETURN islandCount
```

---

# 11. Correctness Argument

We can justify the algorithm in two parts.

## Claim 1: Every island is counted at least once

When scanning the grid, every island contains at least one land cell.

Eventually the scan reaches the first still-unvisited cell belonging to that island.

The algorithm increments the island count.

Therefore every island contributes at least one count.

## Claim 2: No island is counted more than once

When the first land cell of an island is found, DFS visits every land cell connected to it and marks them visited.

Therefore every remaining cell belonging to that island becomes `"0"`.

The outer loops can never count that island again.

Since every island is counted once and only once, the algorithm is correct.

---

# 12. Complexity Analysis

Let:

```text
m = number of rows
n = number of columns
```

There are:

```text
m × n
```

cells.

## Time Complexity

Each cell is visited at most a constant number of times.

Therefore:

```text
O(m × n)
```

Even though each DFS call checks four directions, four is a constant.

Thus:

```text
O(4mn) = O(mn)
```

## Space Complexity

The grid itself is modified, so there is no separate visited matrix.

However, recursive DFS uses the Python call stack.

In the worst case, the entire grid is one long connected island.

Therefore recursive stack depth can approach:

```text
O(m × n)
```

Worst-case auxiliary space:

```text
O(m × n)
```

---

# 13. Why DFS Is a Strong Choice

This problem asks only for connected components.

DFS naturally answers:

> Starting from one land cell, which other land cells belong to the same component?

Once DFS starts from a land cell, it consumes the entire island.

Therefore DFS matches the structure of the problem directly.

Advantages:

- simple implementation,
- natural connected-component traversal,
- optimal `O(mn)` time,
- no additional visited matrix when modifying the grid,
- easy to explain in interviews.

---

# 14. DFS vs BFS vs Union-Find

## Recursive DFS

Advantages:

- shortest implementation,
- intuitive,
- easy to derive.

Disadvantage:

- Python recursion depth may become a problem for large connected grids.

## Iterative DFS

Uses an explicit stack.

```python
stack = [(row, col)]

while stack:
    r, c = stack.pop()
```

Advantages:

- same DFS logic,
- avoids Python recursion-depth issues.

For Python interviews, this is often the safest implementation.

## BFS

Uses a queue.

```python
from collections import deque
```

Advantages:

- avoids recursion,
- natural level-by-level traversal,
- useful if shortest path or distance information becomes relevant.

For pure connected components, DFS and BFS are equally valid.

## Union-Find / Disjoint Set Union

Treat every land cell as a node and union adjacent land cells.

Useful when:

- connectivity changes dynamically,
- cells are added incrementally,
- many connectivity queries are required.

For the static Number of Islands problem, DFS/BFS is simpler.

---

# 15. Iterative DFS Version

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        if not grid:
            return 0

        rows = len(grid)
        cols = len(grid[0])

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        islands = 0

        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == "1":

                    islands += 1

                    stack = [(row, col)]

                    grid[row][col] = "0"

                    while stack:

                        r, c = stack.pop()

                        for dr, dc in directions:

                            nr = r + dr
                            nc = c + dc

                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and grid[nr][nc] == "1"
                            ):

                                grid[nr][nc] = "0"
                                stack.append((nr, nc))

        return islands
```

---

# 16. BFS Version

```python
from typing import List
from collections import deque


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        if not grid:
            return 0

        rows = len(grid)
        cols = len(grid[0])

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        islands = 0

        for row in range(rows):
            for col in range(cols):

                if grid[row][col] == "1":

                    islands += 1

                    queue = deque([(row, col)])

                    grid[row][col] = "0"

                    while queue:

                        r, c = queue.popleft()

                        for dr, dc in directions:

                            nr = r + dr
                            nc = c + dc

                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and grid[nr][nc] == "1"
                            ):

                                grid[nr][nc] = "0"
                                queue.append((nr, nc))

        return islands
```

---

# 17. Test Cases

## Test Case 1 — One Large Island

```python
grid = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
]
```

Expected:

```text
1
```

---

## Test Case 2 — Multiple Islands

```python
grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]
```

Expected:

```text
3
```

---

## Test Case 3 — All Water

```python
grid = [
    ["0","0","0"],
    ["0","0","0"]
]
```

Expected:

```text
0
```

---

## Test Case 4 — All Land

```python
grid = [
    ["1","1","1"],
    ["1","1","1"],
    ["1","1","1"]
]
```

Expected:

```text
1
```

---

## Test Case 5 — Diagonal Cells Do Not Connect

```python
grid = [
    ["1","0","1"],
    ["0","1","0"],
    ["1","0","1"]
]
```

Expected:

```text
5
```

The center cell is diagonally adjacent to four other cells, but diagonal connections do not count.

---

## Test Case 6 — Single Land Cell

```python
grid = [["1"]]
```

Expected:

```text
1
```

---

## Test Case 7 — Single Water Cell

```python
grid = [["0"]]
```

Expected:

```text
0
```

---

## Test Case 8 — One Row

```python
grid = [
    ["1","1","0","1","0","1","1","1"]
]
```

Expected:

```text
3
```

---

## Test Case 9 — One Column

```python
grid = [
    ["1"],
    ["0"],
    ["1"],
    ["1"],
    ["0"],
    ["1"]
]
```

Expected:

```text
3
```

---

## Test Case 10 — Snake-Shaped Island

```python
grid = [
    ["1","1","1","0"],
    ["0","0","1","0"],
    ["1","1","1","0"],
    ["1","0","0","0"]
]
```

Expected:

```text
1
```

This is useful for verifying that the traversal follows arbitrary connected shapes.

---

# 18. Python Implementation Guidance

## Use Strings, Not Integers

LeetCode represents the matrix as:

```python
List[List[str]]
```

Therefore use:

```python
"1"
"0"
```

not:

```python
1
0
```

Correct:

```python
if grid[row][col] == "1":
```

Incorrect:

```python
if grid[row][col] == 1:
```

---

## Bounds Checking

A standard bounds condition is:

```python
0 <= row < rows and 0 <= col < cols
```

or its inverse:

```python
if row < 0 or row >= rows or col < 0 or col >= cols:
    return
```

---

## Direction Array Pattern

For iterative traversal, memorize the idea rather than exact syntax:

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
    nr = r + dr
    nc = c + dc
```

This pattern appears constantly in matrix problems.

---

## Mark Visited When Discovered

In iterative DFS/BFS, mark the neighbor visited before putting it into the stack or queue:

```python
grid[nr][nc] = "0"
stack.append((nr, nc))
```

Do not wait until it is removed from the stack.

Otherwise multiple neighboring cells may add the same cell more than once.

---

# 19. Common Mistakes

## Mistake 1 — Counting Every `"1"`

Wrong idea:

```python
for row:
    for col:
        if grid[row][col] == "1":
            count += 1
```

This counts land cells, not islands.

---

## Mistake 2 — Including Diagonal Neighbors

For this problem:

```text
1 0
0 1
```

contains two islands, not one.

---

## Mistake 3 — Forgetting to Mark Visited

If visited cells remain `"1"`, DFS may repeatedly revisit them and recurse forever.

---

## Mistake 4 — Marking Visited Too Late

For BFS/iterative DFS, marking when popping rather than when pushing can create duplicate queue/stack entries.

---

## Mistake 5 — Using `pop(0)` for BFS

This is inefficient:

```python
queue.pop(0)
```

Use:

```python
from collections import deque
queue.popleft()
```

because `deque.popleft()` is `O(1)`.

---

## Mistake 6 — Ignoring Python Recursion Limits

Recursive DFS is elegant but Python can fail on very deep traversals.

For robust production/interview code, iterative DFS or BFS may be safer.

---

## Mistake 7 — Assuming the Input Should Stay Unchanged

The provided solution destroys the original land representation.

If the interviewer says the input must remain unchanged, use a separate visited structure.

---

# 20. Interview Explanation Template

A concise but strong interview explanation:

> I treat the matrix as an implicit graph where every land cell is a node connected to its four orthogonal land neighbors. I scan every cell. When I find an unvisited land cell, I know I have discovered a new connected component, so I increment the island count. I then run DFS from that cell and mark every reachable land cell visited. Because every cell is processed at most once, the time complexity is O(mn). Recursive DFS can use O(mn) stack space in the worst case, so in Python I can switch to iterative DFS if recursion depth is a concern.

---

# 21. Interview Questions and Answers

This section is deliberately detailed because interviewers often use Number of Islands as a starting point and then modify the requirements.

---

## Easy-Level Interview Questions

### Q1. What data structure concept is hidden behind this matrix problem?

**Answer:**

The matrix represents an implicit graph.

Each land cell is a vertex, and edges connect horizontal and vertical neighboring land cells.

The task is therefore equivalent to counting connected components in a graph.

---

### Q2. Why does each new unvisited `"1"` correspond to exactly one new island?

**Answer:**

If a land cell belonged to an island that had already been discovered, the previous DFS/BFS traversal would already have visited it.

Therefore any land cell that remains unvisited during scanning must belong to a new connected component.

---

### Q3. Why is DFS appropriate here?

**Answer:**

Once an unvisited land cell is found, we need to discover all land reachable from it.

DFS is specifically designed to explore all nodes in a connected component before moving on.

---

### Q4. Can BFS solve the problem too?

**Answer:**

Yes.

DFS and BFS both explore the complete connected component.

The number of times we initiate either traversal equals the number of islands.

---

### Q5. What is the time complexity?

**Answer:**

```text
O(mn)
```

where `m` is the number of rows and `n` is the number of columns.

Each cell is processed at most once as an unvisited land cell.

---

### Q6. Why isn't the time complexity `O(4mn)`?

**Answer:**

Technically each cell checks up to four neighbors, so the operation count is proportional to `4mn`.

Big-O notation ignores constant factors:

```text
O(4mn) = O(mn)
```

---

### Q7. What is the worst-case recursive space complexity?

**Answer:**

```text
O(mn)
```

A worst-case grid can contain one enormous connected island, producing a very deep recursion chain.

---

### Q8. Why can recursive DFS be risky in Python?

**Answer:**

Python has a limited recursion depth.

A sufficiently large or snake-shaped island can produce a `RecursionError`.

An explicit stack avoids this issue.

---

### Q9. What does converting `"1"` to `"0"` accomplish?

**Answer:**

It acts as an in-place visited marker.

After changing a land cell to `"0"`, future traversals treat it as already processed.

---

### Q10. What changes if diagonal cells are also considered connected?

**Answer:**

Add four diagonal directions.

Instead of four neighbors, each cell has up to eight:

```python
directions = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),           (0,1),
    (1,-1),  (1,0),   (1,1)
]
```

The overall algorithm remains unchanged.

---

## Medium-Level Interview Questions

### Q11. If modifying the input grid is forbidden, how would you change the solution?

**Answer:**

Maintain a separate visited structure.

For example:

```python
visited = set()
```

or:

```python
visited = [[False] * cols for _ in range(rows)]
```

A land cell can then be explored only if:

```python
grid[r][c] == "1" and not visited[r][c]
```

Time remains `O(mn)`, while extra memory becomes `O(mn)`.

---

### Q12. Which is better here: `set()` or a boolean visited matrix?

**Answer:**

A boolean matrix usually has lower constant-factor overhead and predictable `O(1)` indexing:

```python
visited[r][c]
```

A set is more flexible and convenient for sparse coordinate spaces:

```python
(r, c) in visited
```

For a dense fixed-size grid, a boolean matrix is often more memory-efficient in lower-level languages, although Python object overhead can complicate the exact comparison.

---

### Q13. Why should BFS mark a cell visited when it is enqueued rather than when it is dequeued?

**Answer:**

Because several neighbors may discover the same cell before it is removed from the queue.

If it is marked only when dequeued, that cell can enter the queue multiple times.

Marking it at discovery ensures each node is enqueued once.

---

### Q14. How would you return the size of every island instead of the number of islands?

**Answer:**

Have DFS/BFS count the number of land cells it visits.

For each newly discovered component:

```python
size = dfs(row, col)
sizes.append(size)
```

DFS can return:

```python
1 + sum(size of valid neighboring branches)
```

or an iterative traversal can increment a local counter.

---

### Q15. How would you return the maximum island size?

**Answer:**

Compute the size of each component and maintain:

```python
max_area = max(max_area, current_area)
```

This is essentially LeetCode 695, **Max Area of Island**.

---

### Q16. How would you count only islands that do not touch the boundary?

**Answer:**

A component touching any of:

```text
row == 0
row == rows - 1
col == 0
col == cols - 1
```

is not enclosed.

Two common approaches:

1. Traverse every island and track whether it touches a boundary.
2. First flood-fill all boundary-connected land, then count what remains.

The second pattern is often cleaner.

---

### Q17. How would you count the perimeter of every island?

**Answer:**

For each land cell, inspect four sides.

A side contributes `1` to the perimeter when:

- it goes outside the grid, or
- the adjacent cell is water.

Thus:

```text
perimeter contribution =
number of sides not touching another land cell
```

---

### Q18. How would you detect whether two islands have the same shape?

**Answer:**

During DFS, record every cell position relative to the component's starting cell.

For example, if the starting cell is `(sr, sc)`, record:

```python
(r - sr, c - sc)
```

Two islands have the same translation-invariant shape if their normalized coordinate sequences match.

This idea appears in **Number of Distinct Islands**.

---

### Q19. Why does DFS order not affect the final number of islands?

**Answer:**

DFS order changes only the order in which cells inside a connected component are visited.

It does not change which cells are reachable.

Every traversal started inside the same connected component eventually reaches the same component, so the number of components remains unchanged.

---

### Q20. Could you scan the grid column-by-column instead of row-by-row?

**Answer:**

Yes.

Traversal order does not affect correctness.

The only requirement is that every cell is eventually considered.

---

### Q21. Suppose land cells are represented by `1` integers rather than `"1"` strings. What changes?

**Answer:**

Only comparisons and assignments:

```python
if grid[r][c] == 1:
    grid[r][c] = 0
```

The algorithm is otherwise identical.

---

### Q22. What happens if the matrix is jagged, meaning rows have different lengths?

**Answer:**

The common implementation assumes a rectangular matrix:

```python
cols = len(grid[0])
```

For a jagged matrix, bounds checks must use:

```python
len(grid[row])
```

for each specific row.

LeetCode 200 uses a rectangular matrix, so the simpler implementation is valid.

---

### Q23. Can you solve the problem without changing the grid and without an `O(mn)` visited structure?

**Answer:**

For a general arbitrary static grid, some form of visited-state tracking is necessary unless the input can be modified.

Without modifying the grid or storing visited information, the algorithm cannot reliably distinguish already-processed land from newly encountered land.

You might compress state or exploit additional constraints, but in the general problem you need either:

- input mutation, or
- explicit visited state.

---

### Q24. What is the difference between graph traversal here and shortest-path BFS?

**Answer:**

Here BFS is used only for **reachability**.

We do not care about distance or levels.

In shortest-path problems, BFS's layer-by-layer ordering matters because the first time a node is reached gives the shortest number of edges in an unweighted graph.

For Number of Islands, either DFS or BFS is sufficient because only connectivity matters.

---

### Q25. What invariant is maintained while scanning the grid?

**Answer:**

After processing all cells before the current scan position, every island touching those processed cells has either:

- been completely visited and erased, or
- not yet been discovered because none of its cells have been encountered.

Thus every remaining `"1"` encountered starts a previously uncounted island.

---

## Difficult-Level Interview Questions

### Q26. How would you solve Number of Islands if land cells are added dynamically over time?

Suppose the grid initially contains only water and operations repeatedly turn cells into land.

**Answer:**

Repeated DFS from scratch would be inefficient.

Use **Disjoint Set Union (Union-Find)**.

For each newly added land cell:

1. create a new component,
2. increment the island count,
3. inspect its four neighbors,
4. union it with each neighboring land component,
5. decrement the island count for every successful union between previously separate components.

This is the main idea behind LeetCode 305, **Number of Islands II**.

With path compression and union by rank/size, each union/find is nearly constant amortized time:

```text
O(alpha(N))
```

where `alpha` is the inverse Ackermann function.

---

### Q27. Why is Union-Find not necessarily the best solution for the original static problem?

**Answer:**

Although Union-Find works, it adds:

- parent arrays,
- rank/size arrays,
- mapping logic,
- union operations.

A simple DFS/BFS already solves the static problem in optimal `O(mn)` time.

Union-Find becomes more compelling when connectivity changes dynamically or many connectivity queries are involved.

---

### Q28. Imagine the grid is too large to fit in memory. How could the problem be approached?

**Answer:**

This becomes a streaming/external-memory connected-components problem.

One possible strategy processes rows incrementally.

Maintain labels for connected land segments in the current and previous rows.

When a segment connects to one or more previous-row segments, merge component labels.

A compact Union-Find structure can maintain active component equivalences.

Once a component can no longer connect to future rows, it can be finalized and its memory released.

This resembles connected-component labeling in image processing.

---

### Q29. How could the solution be parallelized?

**Answer:**

Naively running DFS from multiple cells in parallel creates race conditions because several workers may traverse the same component.

A safer approach is:

1. partition the grid into blocks,
2. compute connected components independently inside each block,
3. assign local component IDs,
4. inspect boundaries between blocks,
5. union local components that touch across partition boundaries,
6. count final global component representatives.

This is essentially parallel connected-component labeling.

---

### Q30. Can the problem be solved in-place without recursion and without an auxiliary stack?

**Answer:**

Not easily in the general case while retaining clean `O(mn)` behavior.

Traversal requires remembering pending cells.

Possible alternatives include:

- encoding traversal state into the matrix,
- scanline flood-fill methods,
- destructive algorithms with more complicated invariants.

For interviews, an explicit stack is the appropriate iterative solution.

---

### Q31. If the grid is extremely sparse, is scanning all `mn` cells still optimal?

**Answer:**

If the input representation itself is a dense matrix, reading the input already costs `O(mn)`.

However, if land positions are provided directly as a sparse coordinate set, then it may be better to operate only on those `k` land cells.

Store land cells in a hash set and traverse neighboring coordinates.

Then complexity can depend on `k` instead of `mn`.

---

### Q32. How would you count islands under toroidal/wrap-around boundaries?

For example, the left and right edges connect.

**Answer:**

Neighbor coordinates must wrap using modulo:

```python
nr = (r + dr) % rows
nc = (c + dc) % cols
```

Care must be taken because ordinary bounds checks no longer apply.

The connected-component algorithm itself remains the same.

---

### Q33. How would you count islands when cells can have different terrain types?

Suppose:

```text
A A B
A B B
C C B
```

and cells connect only when their terrain type matches.

**Answer:**

Each DFS starts from a cell and stores its terrain type.

Neighbors are traversed only when:

```python
grid[nr][nc] == terrain_type
```

The problem becomes counting connected regions of equal labels.

---

### Q34. What if each cell has weighted edges and the interviewer asks for minimum cost to connect islands?

**Answer:**

The problem is no longer simply connected-component counting.

Possible next steps depend on the exact formulation.

Examples:

- shortest bridge between two islands → BFS from one island,
- minimum total cost to connect many islands → potentially construct an island-level weighted graph and apply MST algorithms,
- weighted cell traversal → Dijkstra's algorithm may become relevant.

The key interview skill is recognizing when plain DFS/BFS is no longer sufficient.

---

### Q35. How would you prove each cell is visited only once?

**Answer:**

A land cell is marked `"0"` immediately upon first discovery.

The traversal condition permits recursion/stack insertion only for cells equal to `"1"`.

Therefore after the first visit, that cell can never again satisfy the traversal condition.

Hence each land cell enters active traversal at most once.

---

### Q36. What pathological shape is particularly dangerous for recursive DFS in Python?

**Answer:**

A long one-cell-wide snake.

For example, imagine one connected component containing tens of thousands of cells arranged so DFS repeatedly moves into exactly one unvisited neighbor.

The recursion depth can approach the number of cells, easily exceeding Python's recursion limit.

---

### Q37. Is recursion depth necessarily equal to island size?

**Answer:**

No.

Recursion depth depends on the DFS traversal path and shape of the component.

A compact island may have many cells but a shallower DFS stack than a long snake-shaped island.

However, worst-case depth can still reach `O(mn)`.

---

### Q38. Suppose an interviewer asks for the number of islands after changing exactly one `0` to `1`. How would you think about it?

**Answer:**

For each candidate water cell, turning it into land can:

- create one new island if no adjacent land exists,
- keep the count unchanged if it touches exactly one existing island,
- reduce the count if it connects multiple previously separate islands.

A naive approach recomputes the answer for every candidate.

A stronger approach first labels every existing island with a unique component ID, then for each zero cell inspects the set of distinct neighboring component IDs.

This lets you reason about its effect locally.

---

### Q39. How would you compute the largest island obtainable by changing one `0` to `1`?

**Answer:**

This is closely related to LeetCode 827, **Making A Large Island**.

Approach:

1. DFS-label each island with a unique ID.
2. Record each island's area.
3. For every zero cell:
   - collect distinct neighboring island IDs,
   - sum their areas,
   - add `1` for the flipped cell.
4. Track the maximum.

The important detail is using a set of component IDs so the same island is not counted twice.

---

### Q40. How would you detect whether an island contains a cycle?

**Answer:**

Treat the land cells as an undirected graph.

During DFS, track the parent cell.

If a neighboring land cell is already visited and is not the parent, then a cycle exists.

This is a standard undirected graph cycle-detection pattern adapted to a grid.

---

### Q41. Can an island graph actually contain cycles?

**Answer:**

Yes.

Example:

```text
1 1
1 1
```

The four cells form a cycle:

```text
top-left
→ top-right
→ bottom-right
→ bottom-left
→ top-left
```

Although cycle detection is irrelevant for counting components, it becomes relevant in interview extensions.

---

### Q42. If you were designing an API for repeated queries on the same immutable grid, what preprocessing might help?

**Answer:**

Run a one-time connected-component labeling pass.

Assign each land cell a component ID and store metadata per component:

```text
component size
perimeter
bounding box
whether it touches boundary
```

Later queries can be answered quickly from the labels without re-running DFS.

---

### Q43. How does this problem relate to image processing?

**Answer:**

Binary images often represent foreground/background pixels.

Finding separate objects in a binary image is exactly connected-component labeling.

Four-neighbor connectivity corresponds to 4-connectivity.

Including diagonals corresponds to 8-connectivity.

Number of Islands is therefore a simplified version of a common computer-vision primitive.

---

### Q44. How does this problem relate to distributed systems or cluster analysis?

**Answer:**

The abstraction is broader than grids.

The underlying task is:

> Group entities according to reachability under a local connection rule.

Examples include:

- network components,
- social graph communities under simple connectivity,
- mesh components,
- image regions,
- occupied sites in percolation models,
- connected clusters in simulations.

The same DFS/BFS connected-component pattern applies.

---

### Q45. If an interviewer asks "Why is DFS optimal?", what should you say carefully?

**Answer:**

It is optimal asymptotically for a dense matrix because every cell may need to be inspected.

Any correct algorithm can be forced to distinguish cases that differ in the final uninspected cell, so in the worst case it must examine `mn` cells.

DFS achieves `O(mn)`, matching that lower bound.

Therefore its time complexity is asymptotically optimal.

---

# 22. Follow-Up Questions Interviewers Commonly Ask

Be prepared for these immediate modifications:

```text
1. What if diagonal connections count?
2. What if the grid cannot be modified?
3. What if the grid is too large for recursion?
4. Return the area of each island.
5. Return the maximum island area.
6. Return island perimeters.
7. Count only closed islands.
8. Find distinct island shapes.
9. Dynamically add land cells.
10. Find the shortest distance between islands.
11. Flip one water cell to maximize area.
12. Label every island with a unique ID.
13. Count components in a sparse grid.
14. Process the grid in parallel.
15. Process a grid too large to fit in memory.
```

These variations test whether you understand the pattern rather than memorizing one solution.

---

# 23. Similar LeetCode Problems

## Strongly Recommended

### LeetCode 695 — Max Area of Island

Same DFS/BFS idea, but compute component size.

### LeetCode 733 — Flood Fill

The simplest flood-fill practice problem.

### LeetCode 994 — Rotting Oranges

Grid traversal where BFS levels represent elapsed time.

### LeetCode 130 — Surrounded Regions

Excellent boundary-flood-fill problem.

### LeetCode 417 — Pacific Atlantic Water Flow

Uses graph reachability in reverse.

### LeetCode 1020 — Number of Enclaves

Boundary-connected component reasoning.

### LeetCode 1254 — Number of Closed Islands

Count components that do not reach the boundary.

### LeetCode 1905 — Count Sub Islands

Compare connected components between two grids.

### LeetCode 463 — Island Perimeter

Grid-neighbor reasoning without full DFS being strictly necessary.

### LeetCode 827 — Making A Large Island

Component labeling plus hypothetical merging.

---

## More Advanced

### LeetCode 305 — Number of Islands II

Dynamic connectivity and Union-Find.

### LeetCode 694 — Number of Distinct Islands

Store normalized island shapes.

### LeetCode 711 — Number of Distinct Islands II

Adds rotations and reflections.

### LeetCode 934 — Shortest Bridge

DFS to identify one island, then BFS to reach another.

### LeetCode 1162 — As Far from Land as Possible

Multi-source BFS.

### LeetCode 1091 — Shortest Path in Binary Matrix

8-direction BFS shortest path.

### LeetCode 542 — 01 Matrix

Multi-source BFS distance propagation.

### LeetCode 286 — Walls and Gates

Multi-source BFS pattern.

### LeetCode 200 — Number of Islands

The fundamental connected-component grid problem.

---

# 24. Non-LeetCode Practice Exercises

These are intended to force transfer of the underlying idea.

---

## Exercise 1 — Count Forest Regions

A map contains:

```text
T = tree
. = empty
```

Trees connected vertically or horizontally form one forest.

Return the number of forests.

### Test Case

```text
T T . . T
T . . . T
. . T T .
. . . T .
```

Expected:

```text
3
```

---

## Exercise 2 — Largest Connected Server Cluster

You receive a binary matrix where:

```text
1 = active server
0 = inactive server
```

Adjacent active servers communicate horizontally or vertically.

Return the size of the largest connected cluster.

### Test Case

```text
1 1 0 0
1 0 0 1
0 0 1 1
0 1 1 1
```

Expected:

```text
6
```

---

## Exercise 3 — Count Rooms in a Floor Plan

A floor plan contains:

```text
. = open floor
# = wall
```

Orthogonally connected open cells belong to the same room.

Return the number of rooms.

### Test Case

```text
..##.
..##.
#####
...##
...##
```

Expected:

```text
3
```

---

## Exercise 4 — Count Diagonally Connected Pixel Objects

A binary image considers all eight neighboring pixels connected.

Return the number of objects.

### Test Case

```text
1 0 0
0 1 0
0 0 1
```

Expected:

```text
1
```

because diagonal connectivity is allowed.

---

## Exercise 5 — Largest Lake

A map uses:

```text
W = water
L = land
```

Return the largest orthogonally connected body of water.

### Test Case

```text
W W L W
W L L W
L L W W
W W W L
```

Expected:

```text
7
```

---

## Exercise 6 — Number of Closed Grass Patches

A map has grass cells `"G"` and empty cells `"."`.

A grass patch is closed if no cell in the patch touches the border.

Return the number of closed patches.

### Test Case

```text
.....
.GG..
.GG..
...G.
.....
```

Expected:

```text
2
```

---

## Exercise 7 — Warehouse Zones

A warehouse floor is represented as integers.

Cells with the same positive integer belong to the same type of storage zone.

Two cells are part of the same zone only if:

- they contain the same integer,
- they are orthogonally adjacent.

Return the total number of connected zones.

### Test Case

```text
1 1 2 2
1 3 3 2
4 4 3 2
4 5 5 5
```

Expected:

```text
5
```

---

## Exercise 8 — Distinct Island Shapes

Return the number of unique island shapes, ignoring translation.

### Test Case

```text
1 1 0 1 1
1 0 0 1 0
0 0 0 0 0
1 1 1 0 1
```

Challenge:

Decide which islands have identical shapes after normalizing their coordinates.

---

## Exercise 9 — Dynamic Land Addition

Start with a `4 x 4` water grid.

Operations:

```text
add(0,0)
add(0,1)
add(2,2)
add(1,1)
add(1,2)
```

After each operation, output the number of islands.

Expected sequence:

```text
1, 1, 2, 2, 1
```

Try solving this efficiently using Union-Find.

---

## Exercise 10 — Shortest Bridge Between Two Land Masses

A matrix contains exactly two islands.

You may convert water cells into land.

Return the minimum number of water cells that must be converted to connect the islands.

### Test Case

```text
0 1 0
0 0 0
0 0 1
```

Expected:

```text
2
```

Hint:

Use DFS to identify one island and multi-source BFS to expand toward the second.

---

# 25. Mini Coding Drills

Try implementing each without looking at a previous solution.

## Drill A

Write recursive DFS for four-direction traversal.

## Drill B

Rewrite it using an explicit stack.

## Drill C

Rewrite it using BFS and `deque`.

## Drill D

Use a separate boolean visited matrix without modifying input.

## Drill E

Modify the solution to count island sizes.

## Drill F

Return the largest island.

## Drill G

Return the number of islands touching the boundary.

## Drill H

Return the number of islands not touching the boundary.

## Drill I

Support eight-direction connectivity.

## Drill J

Label every island with a unique integer ID.

---

# 26. Useful General Grid Template

A reusable iterative traversal template:

```python
rows = len(grid)
cols = len(grid[0])

directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

for r in range(rows):
    for c in range(cols):

        if should_start_traversal(r, c):

            stack = [(r, c)]
            mark_visited(r, c)

            while stack:

                cr, cc = stack.pop()

                for dr, dc in directions:

                    nr = cr + dr
                    nc = cc + dc

                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and is_valid_neighbor(nr, nc)
                    ):

                        mark_visited(nr, nc)
                        stack.append((nr, nc))
```

If you understand this template conceptually, dozens of matrix problems become variations of the same idea.

---

# 27. General Connected-Components Template

The matrix version is equivalent to:

```python
components = 0

for node in graph:

    if node not in visited:

        components += 1

        dfs(node)
```

That relationship is worth remembering.

Number of Islands is not fundamentally about islands.

It is about:

```text
CONNECTED COMPONENTS
```

---

# 28. How to Recognize Similar Problems

Look for phrases such as:

```text
connected region
group
cluster
component
reachable
adjacent cells
contiguous region
same group
flood fill
neighboring cells
```

These often signal DFS/BFS.

Then ask:

```text
1. What represents a node?
2. What represents an edge?
3. How do I identify valid neighbors?
4. Do I need connectivity, shortest path, or both?
5. How will I mark visited states?
```

If the requirement is merely connectivity, DFS or BFS is usually enough.

If minimum distance is required in an unweighted graph, BFS becomes especially important.

If connectivity changes dynamically, consider Union-Find.

---

# 29. DFS, BFS, and Union-Find Decision Table

| Requirement | Preferred Tool |
|---|---|
| Count static connected components | DFS / BFS |
| Explore one component | DFS / BFS |
| Largest component | DFS / BFS |
| Shortest unweighted path | BFS |
| Distance from many sources | Multi-source BFS |
| Dynamic connectivity | Union-Find |
| Detect cycle in undirected graph | DFS / Union-Find |
| Topological dependency ordering | DFS / Kahn's BFS |
| Weighted shortest path | Dijkstra / related algorithms |

---

# 30. Interview Strategy

When presented with Number of Islands:

1. Clarify whether diagonal connectivity counts.
2. Clarify whether modifying the input is allowed.
3. State that the grid is an implicit graph.
4. Explain connected components.
5. Propose DFS or BFS.
6. State the visited strategy.
7. Derive `O(mn)` time.
8. Mention recursive-stack concerns in Python.
9. Implement cleanly.
10. Test:
   - all water,
   - all land,
   - separate single cells,
   - diagonal land,
   - one long component.

This sequence demonstrates structured problem solving.

---

# 31. Final Mental Model

The most important idea to retain is:

```text
Encounter unvisited land
        ↓
New connected component
        ↓
Increment answer
        ↓
Flood-fill the entire component
        ↓
Continue scanning
```

Or in one sentence:

> Every time the outer scan finds land that has not already been consumed by a previous traversal, it has found exactly one new island.

---

# 32. Suggested Learning Progression

A strong sequence for mastering this family is:

```text
733  Flood Fill
 ↓
200  Number of Islands
 ↓
695  Max Area of Island
 ↓
994  Rotting Oranges
 ↓
130  Surrounded Regions
 ↓
417  Pacific Atlantic Water Flow
 ↓
1020 Number of Enclaves
 ↓
1254 Number of Closed Islands
 ↓
934  Shortest Bridge
 ↓
827  Making A Large Island
 ↓
305  Number of Islands II
```

The progression moves from basic traversal to:

- connected components,
- component metadata,
- multi-source BFS,
- boundary reasoning,
- reverse reachability,
- component merging,
- dynamic connectivity.

---

# 33. Key Takeaways

- A matrix can often be interpreted as an implicit graph.
- Number of Islands is a connected-components problem.
- DFS and BFS both solve it in `O(mn)`.
- Marking visited cells prevents double counting.
- Modifying the grid avoids a separate visited matrix.
- Recursive DFS is elegant but may hit Python recursion limits.
- Iterative DFS is an excellent default for Python interviews.
- BFS becomes particularly important when shortest distances or propagation times are involved.
- Union-Find becomes important when connectivity changes dynamically.
- The deeper pattern matters much more than memorizing one implementation.

Master this problem well because it is one of the foundational templates behind a large class of graph, matrix, image-processing, and connectivity interview questions.
