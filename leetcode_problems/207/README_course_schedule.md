# LeetCode 207 — Course Schedule

## Interview Study README

**Difficulty:** Medium  
**Core topics:** Directed Graphs, Cycle Detection, Topological Sort  
**Primary solution:** Kahn's Algorithm (BFS / indegree processing)  
**Alternative solution:** DFS with 3-state visitation

---

# 1. Problem Statement

There are `numCourses` courses labeled from `0` to `numCourses - 1`.

You are given:

```python
prerequisites
```

where:

```python
[a, b]
```

means:

> You must finish course `b` before course `a`.

Return `True` if every course can be finished. Otherwise return `False`.

Example:

```python
numCourses = 2
prerequisites = [[1, 0]]
```

This means:

```text
0 -> 1
```

so the answer is:

```python
True
```

But:

```python
numCourses = 2
prerequisites = [[1, 0], [0, 1]]
```

gives:

```text
0 -> 1
^    |
|____|
```

and therefore:

```python
False
```

because both courses wait for each other.

---

# 2. What Is the Problem Really Asking?

This is a directed graph problem.

Each course is a node.

For:

```python
[a, b]
```

we create:

```text
b -> a
```

because `b` must be completed before `a`.

The real question is:

> Does the directed graph contain a cycle?

If a cycle exists:

```text
A -> B -> C -> A
```

then:

```text
A waits for C
C waits for B
B waits for A
```

Nobody in that cycle can start.

Therefore:

```text
Can finish all courses
<=> no directed cycle exists
```

Equivalently:

```text
Can finish all courses
<=> a topological ordering exists
```

---

# 3. The Best Memory Model: Blockers and Unlocking

Kahn's Algorithm becomes much easier if you stop thinking about graph terminology first.

Imagine a project with tasks.

Each task may have blockers.

Example:

```text
Task A: 0 blockers
Task B: 1 blocker
Task C: 1 blocker
Task D: 2 blockers
```

A task with zero blockers is ready.

When you finish a task, you remove one blocker from every task waiting for it.

If one of those tasks reaches zero blockers, it becomes ready.

That is Kahn's Algorithm.

Remember:

```text
COUNT blockers
QUEUE zero-blocker tasks
DO one task
UNLOCK dependents
CHECK whether everything finished
```

Short mnemonic:

```text
COUNT -> QUEUE -> DO -> UNLOCK -> CHECK
```

---

# 4. The Padlock Analogy

Suppose Course 3 requires Courses 1 and 2.

Visualize:

```text
Course 3
[LOCK] [LOCK]
```

So:

```python
indegree[3] = 2
```

Finish Course 1:

```text
Course 3
[LOCK]
```

Now:

```python
indegree[3] = 1
```

Finish Course 2:

```text
Course 3
UNLOCKED
```

Now:

```python
indegree[3] = 0
```

Only then can Course 3 enter the queue.

So:

```text
indegree = number of remaining padlocks
```

and:

```text
indegree == 0 = ready to take
```

---

# 5. Meaning of Every Kahn Variable

| Code | Real-world meaning |
|---|---|
| `graph[x]` | Which courses are waiting for `x`? |
| `indegree[x]` | How many unfinished prerequisites still block `x`? |
| `queue` | Courses ready to take now |
| `popleft()` | Finish one ready course |
| `indegree[next] -= 1` | Remove one blocker |
| `indegree[next] == 0` | Course has just become available |
| `completed` | Number of courses successfully finished |
| `completed == numCourses` | Everything was eventually finishable |

This table is the core of the entire problem.

---

# 6. Main Example

```python
numCourses = 4

prerequisites = [
    [1, 0],
    [2, 0],
    [3, 1],
    [3, 2]
]
```

Interpretation:

```text
0 -> 1
0 -> 2
1 -> 3
2 -> 3
```

Graph:

```text
      1
     / \
    0   3
     \ /
      2
```

Valid orders include:

```text
0, 1, 2, 3
```

and:

```text
0, 2, 1, 3
```

The problem only asks whether at least one valid order exists.

---

# 7. What Is Topological Sort?

A topological ordering is an ordering of nodes such that every prerequisite appears before the node that depends on it.

For:

```text
0 -> 1
0 -> 2
1 -> 3
2 -> 3
```

valid orders include:

```text
0, 1, 2, 3
```

and:

```text
0, 2, 1, 3
```

A topological ordering exists if and only if the directed graph is acyclic.

Therefore:

```text
Course Schedule
= directed cycle detection
= existence of a topological ordering
```

---

# 8. Kahn's Algorithm — Step by Step

## Step 1: Build the adjacency list

```python
graph = [[] for _ in range(numCourses)]
```

For every:

```python
[course, prerequisite]
```

do:

```python
graph[prerequisite].append(course)
```

This means:

> When I finish this prerequisite, which courses should I re-check?

For the main example:

```python
graph = [
    [1, 2],
    [3],
    [3],
    []
]
```

Interpretation:

```text
Finish 0 -> check 1 and 2
Finish 1 -> check 3
Finish 2 -> check 3
Finish 3 -> nobody depends on it
```

## Step 2: Count blockers

```python
indegree = [0] * numCourses
```

For every prerequisite pair:

```python
indegree[course] += 1
```

For our example:

```python
indegree = [0, 1, 1, 2]
```

Meaning:

```text
Course 0 = 0 blockers
Course 1 = 1 blocker
Course 2 = 1 blocker
Course 3 = 2 blockers
```

## Step 3: Queue every unlocked course

```python
queue = deque()

for course in range(numCourses):
    if indegree[course] == 0:
        queue.append(course)
```

Initially:

```text
queue = [0]
```

## Step 4: Repeatedly finish and unlock

```python
while queue:

    course = queue.popleft()
    completed += 1

    for next_course in graph[course]:

        indegree[next_course] -= 1

        if indegree[next_course] == 0:
            queue.append(next_course)
```

## Step 5: Check whether everything finished

```python
return completed == numCourses
```

---

# 9. Complete Kahn Solution

```python
from collections import deque
from typing import List


class Solution:
    def canFinish(
        self,
        numCourses: int,
        prerequisites: List[List[int]]
    ) -> bool:

        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        # Build graph and count blockers.
        for course, prerequisite in prerequisites:

            graph[prerequisite].append(course)

            indegree[course] += 1

        queue = deque()

        # Initially available courses.
        for course in range(numCourses):

            if indegree[course] == 0:
                queue.append(course)

        completed = 0

        while queue:

            course = queue.popleft()

            completed += 1

            # Completing this course removes one blocker
            # from every dependent course.
            for next_course in graph[course]:

                indegree[next_course] -= 1

                if indegree[next_course] == 0:
                    queue.append(next_course)

        return completed == numCourses
```

---

# 10. Granular Dry Run

Input:

```python
numCourses = 4

prerequisites = [
    [1, 0],
    [2, 0],
    [3, 1],
    [3, 2]
]
```

## Build graph

Start:

```python
graph = [[], [], [], []]
```

Process `[1, 0]`:

```text
0 -> 1
```

Now:

```python
graph = [[1], [], [], []]
```

Process `[2, 0]`:

```text
0 -> 2
```

Now:

```python
graph = [[1, 2], [], [], []]
```

Process `[3, 1]`:

```text
1 -> 3
```

Now:

```python
graph = [[1, 2], [3], [], []]
```

Process `[3, 2]`:

```text
2 -> 3
```

Final:

```python
graph = [[1, 2], [3], [3], []]
```

## Build indegree

Start:

```python
[0, 0, 0, 0]
```

After `[1, 0]`:

```python
[0, 1, 0, 0]
```

After `[2, 0]`:

```python
[0, 1, 1, 0]
```

After `[3, 1]`:

```python
[0, 1, 1, 1]
```

After `[3, 2]`:

```python
[0, 1, 1, 2]
```

## Initialize queue

Only Course 0 has zero blockers:

```python
queue = deque([0])
completed = 0
```

## Iteration 1

Pop:

```text
0
```

Now:

```text
completed = 1
```

Course 0 unlocks Courses 1 and 2.

```text
indegree[1]: 1 -> 0
indegree[2]: 1 -> 0
```

Queue:

```text
[1, 2]
```

Indegree:

```python
[0, 0, 0, 2]
```

## Iteration 2

Pop:

```text
1
```

Now:

```text
completed = 2
```

Course 1 removes one blocker from Course 3:

```text
indegree[3]: 2 -> 1
```

Course 3 is still blocked because Course 2 is unfinished.

Queue:

```text
[2]
```

## Iteration 3

Pop:

```text
2
```

Now:

```text
completed = 3
```

Course 2 removes Course 3's final blocker:

```text
indegree[3]: 1 -> 0
```

Course 3 enters queue:

```text
queue = [3]
```

## Iteration 4

Pop:

```text
3
```

Now:

```text
completed = 4
```

No course depends on Course 3.

Queue becomes empty.

Finally:

```python
completed == numCourses
```

is:

```text
4 == 4
```

Therefore:

```python
True
```

---

# 11. Dry Run State Table

| Step | Course popped | Queue after pop | Indegree change | Queue after updates | Completed |
|---|---:|---|---|---|---:|
| Initial | — | `[0]` | — | `[0]` | 0 |
| 1 | 0 | `[]` | `1:1->0`, `2:1->0` | `[1,2]` | 1 |
| 2 | 1 | `[2]` | `3:2->1` | `[2]` | 2 |
| 3 | 2 | `[]` | `3:1->0` | `[3]` | 3 |
| 4 | 3 | `[]` | none | `[]` | 4 |

---

# 12. How a Cycle Appears in Kahn's Algorithm

Consider:

```python
numCourses = 3

prerequisites = [
    [1, 0],
    [2, 1],
    [0, 2]
]
```

Graph:

```text
0 -> 1 -> 2
^         |
|_________|
```

Every course has one blocker:

```python
indegree = [1, 1, 1]
```

So:

```python
queue = deque([])
```

Nothing can begin.

Thus:

```text
completed = 0
numCourses = 3
```

and:

```python
completed == numCourses
```

is false.

Real interpretation:

```text
0 waits for 2
2 waits for 1
1 waits for 0
```

Everyone waits forever.

---

# 13. Why Kahn's Algorithm Is Correct

Kahn repeatedly removes nodes with indegree zero.

A zero-indegree node has no unresolved prerequisite, so it can safely appear next in a valid topological ordering.

When that node is removed, its outgoing edges are effectively removed too.

That can create new zero-indegree nodes.

If the graph is a DAG, this process can continue until every node is removed.

If the process stops early, every remaining node has at least one incoming edge from another remaining node.

In a finite directed graph, repeatedly following those incoming edges must eventually revisit a node.

That creates a cycle.

Therefore:

```text
processed all nodes -> acyclic
stopped early -> cycle exists
```

---

# 14. Formal Useful Fact

Every finite DAG has at least one zero-indegree node.

Proof by contradiction:

Assume a finite DAG has no zero-indegree node.

Then every node has at least one incoming edge.

Pick any node and repeatedly follow an incoming edge backward.

Because there are finitely many nodes, eventually some node must repeat.

That repetition creates a directed cycle.

Contradiction.

Therefore every finite DAG has a zero-indegree node.

This fact is the mathematical foundation of Kahn's Algorithm.

---

# 15. Pseudocode

```text
FUNCTION canFinish(numCourses, prerequisites):

    CREATE graph with one adjacency list per course
    CREATE indegree array initialized to zero

    FOR each [course, prerequisite]:

        add course to graph[prerequisite]

        indegree[course] += 1

    CREATE empty queue

    FOR every course:

        IF indegree[course] == 0:
            add course to queue

    completed = 0

    WHILE queue not empty:

        course = remove front

        completed += 1

        FOR each next_course depending on course:

            indegree[next_course] -= 1

            IF indegree[next_course] == 0:
                add next_course to queue

    RETURN completed == numCourses
```

---

# 16. Complexity

Let:

```text
V = numCourses
E = len(prerequisites)
```

Building the graph:

```text
O(E)
```

Scanning for initial zero-indegree nodes:

```text
O(V)
```

During Kahn's BFS:

- each node is processed at most once
- each edge is examined at most once

Therefore total time:

```text
O(V + E)
```

Space:

```text
O(V + E)
```

for:

- adjacency list
- indegree array
- queue

This is asymptotically optimal because every node and dependency may need inspection.

---

# 17. Why Use an Adjacency List?

Adjacency matrix:

```python
[[0] * V for _ in range(V)]
```

requires:

```text
O(V^2)
```

space.

Adjacency list:

```python
graph = [[] for _ in range(V)]
```

requires:

```text
O(V + E)
```

space.

Dependency graphs are often sparse, so adjacency lists are the standard choice.

---

# 18. Alternative Solution: DFS Three-State Cycle Detection

The second canonical solution uses DFS.

States:

```text
0 = unvisited
1 = currently visiting
2 = fully processed
```

A cycle exists if DFS reaches a node that is already:

```text
state == 1
```

because that node is still on the current recursion path.

---

# 19. Complete DFS Solution

```python
from typing import List


class Solution:
    def canFinish(
        self,
        numCourses: int,
        prerequisites: List[List[int]]
    ) -> bool:

        graph = [[] for _ in range(numCourses)]

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)

        state = [0] * numCourses

        def dfs(course):

            if state[course] == 1:
                return False

            if state[course] == 2:
                return True

            state[course] = 1

            for next_course in graph[course]:

                if not dfs(next_course):
                    return False

            state[course] = 2

            return True

        for course in range(numCourses):

            if state[course] == 0:

                if not dfs(course):
                    return False

        return True
```

---

# 20. Why DFS Needs Three States

Consider:

```text
0 -> 1 -> 3
 \       ^
  -> 2 --|
```

There is no cycle.

DFS may reach Course 3 through Course 1 and later reach it again through Course 2.

So:

```text
already visited
```

does not automatically mean:

```text
cycle
```

We need to know whether the node is:

```text
currently on the recursion path
```

or:

```text
already completely processed
```

Hence:

```text
0 = unseen
1 = active recursion path
2 = verified safe
```

---

# 21. Kahn vs DFS

| Feature | Kahn BFS | DFS |
|---|---|---|
| Main idea | Repeatedly unlock zero-indegree nodes | Detect a back edge |
| Main state | `indegree` | `state = 0/1/2` |
| Cycle signal | Not all nodes processed | Reach a `visiting` node |
| Queue/stack | Queue | Recursion stack |
| Natural topological order | Yes | Yes, if recorded on exit |
| Python recursion depth concern | No | Yes |
| Time | `O(V+E)` | `O(V+E)` |
| Space | `O(V+E)` | `O(V+E)` |

For Course Schedule, Kahn's Algorithm is often the easiest one to explain using the blocker mental model.

---

# 22. Python Implementation Guidance

## Use `deque`

```python
from collections import deque
```

Use:

```python
queue.popleft()
```

because it is `O(1)`.

Avoid:

```python
list.pop(0)
```

because that is `O(n)`.

## Use descriptive variable names

Prefer:

```python
course
prerequisite
next_course
indegree
completed
```

over vague names such as:

```python
x
y
arr
cnt
```

especially in graph interviews.

## Keep edge direction explicit

For:

```python
[course, prerequisite]
```

write mentally:

```text
prerequisite -> course
```

before coding.

---

# 23. Common Mistakes

## Mistake 1: Wrong edge direction

Input:

```python
[a, b]
```

means:

```text
b -> a
```

not:

```text
a -> b
```

## Mistake 2: Thinking indegree is fixed forever

During Kahn's Algorithm, indegree changes.

It means:

```text
remaining unresolved prerequisites
```

not merely original prerequisite count.

## Mistake 3: Using ordinary `visited` for DFS cycle detection

Directed cycle detection requires distinguishing:

```text
visiting
```

from:

```text
fully processed
```

## Mistake 4: Checking only direct two-node cycles

Cycles can be arbitrarily long.

Example:

```text
0 -> 1 -> 2 -> 3 -> 4 -> 0
```

## Mistake 5: Forgetting disconnected components

A graph may contain:

```text
0 -> 1

2 -> 3

4
```

All components must be considered.

## Mistake 6: Confusing Kahn BFS with shortest-path BFS

Here the queue does not represent distance.

It represents:

```text
currently available zero-blocker tasks
```

---

# 24. Test Cases

## Test 1 — One prerequisite

```python
numCourses = 2
prerequisites = [[1, 0]]
```

Expected:

```python
True
```

## Test 2 — Two-node cycle

```python
numCourses = 2
prerequisites = [[1, 0], [0, 1]]
```

Expected:

```python
False
```

## Test 3 — No prerequisites

```python
numCourses = 5
prerequisites = []
```

Expected:

```python
True
```

## Test 4 — Long chain

```python
numCourses = 5

prerequisites = [
    [1, 0],
    [2, 1],
    [3, 2],
    [4, 3]
]
```

Expected:

```python
True
```

## Test 5 — Long cycle

```python
numCourses = 5

prerequisites = [
    [1, 0],
    [2, 1],
    [3, 2],
    [4, 3],
    [0, 4]
]
```

Expected:

```python
False
```

## Test 6 — Disconnected DAG

```python
numCourses = 6

prerequisites = [
    [1, 0],
    [2, 1],
    [4, 3]
]
```

Expected:

```python
True
```

## Test 7 — One cyclic component

```python
numCourses = 6

prerequisites = [
    [1, 0],
    [2, 1],
    [4, 3],
    [3, 4]
]
```

Expected:

```python
False
```

## Test 8 — Diamond

```python
numCourses = 4

prerequisites = [
    [1, 0],
    [2, 0],
    [3, 1],
    [3, 2]
]
```

Expected:

```python
True
```

## Test 9 — Multiple starting nodes

```python
numCourses = 5

prerequisites = [
    [2, 0],
    [2, 1],
    [4, 3]
]
```

Expected:

```python
True
```

Initially available:

```text
0, 1, 3
```

## Test 10 — Self-loop

```python
numCourses = 1
prerequisites = [[0, 0]]
```

Expected:

```python
False
```

---

# 25. Interview Questions — Easy

## Q1. What kind of graph is this?

**Answer:**  
A directed graph. Every prerequisite defines a direction: prerequisite first, dependent course second.

## Q2. What does `[a, b]` mean?

**Answer:**  
Course `a` requires Course `b`, so create edge:

```text
b -> a
```

## Q3. What does indegree mean?

**Answer:**  
The number of incoming edges. In this problem it means the number of unfinished prerequisites still blocking a course.

## Q4. Why do zero-indegree nodes enter the queue?

**Answer:**  
They have no unresolved prerequisites and can be taken immediately.

## Q5. What does `graph[x]` mean in the Kahn implementation?

**Answer:**  
The courses that directly depend on Course `x`.

## Q6. Why do we decrement indegree?

**Answer:**  
Completing a prerequisite satisfies one requirement of every dependent course.

## Q7. When does a dependent course enter the queue?

**Answer:**  
When its remaining indegree becomes zero.

## Q8. What is a cycle here?

**Answer:**  
A circular prerequisite relationship in which every course waits on another course in the same loop.

## Q9. What is the time complexity?

**Answer:**  
`O(V + E)`.

## Q10. Why use `deque`?

**Answer:**  
`popleft()` is `O(1)`, which is appropriate for queue processing.

---

# 26. Interview Questions — Medium

## Q11. Why does `completed < numCourses` indicate a cycle?

**Answer:**  
If the queue becomes empty while nodes remain, every remaining node still has positive indegree. Each is waiting on another remaining node. Following those dependencies in a finite graph must eventually revisit a node, which creates a cycle.

## Q12. Can a DAG have no zero-indegree node?

**Answer:**  
No. If every node had an incoming edge, repeatedly following incoming edges would eventually revisit a node, creating a cycle.

## Q13. Can multiple zero-indegree nodes exist?

**Answer:**  
Yes. They represent multiple tasks that are independently ready.

Example:

```text
0 -> 2
1 -> 2
```

Both 0 and 1 initially have indegree zero.

## Q14. Does Kahn always produce the same order?

**Answer:**  
No. If multiple zero-indegree nodes are available, different processing orders can produce different valid topological orders.

## Q15. How do you generate the lexicographically smallest topological order?

**Answer:**  
Use a min-heap instead of a FIFO queue so that the smallest available node is always processed first.

## Q16. Why is this still called BFS if we are not finding shortest distance?

**Answer:**  
Because BFS refers broadly to queue-based graph traversal. Here the queue represents ready nodes rather than equal-distance nodes.

## Q17. How is Course Schedule II different?

**Answer:**  
Course Schedule II asks for the actual order. Store each processed node in:

```python
order.append(course)
```

and return `order` if all nodes were processed.

## Q18. Why does DFS need 3 states?

**Answer:**  
Because an already seen node might either be on the current recursion path or already fully processed. Only the former indicates a cycle.

## Q19. Why does encountering a `visiting` node prove a cycle?

**Answer:**  
A `visiting` node is an ancestor in the current recursion path. An edge back to it closes a directed loop.

## Q20. Why is reaching a `processed` node safe?

**Answer:**  
It means that node and everything reachable from it have already been checked without finding a cycle.

---

# 27. Interview Questions — Difficult

## Q21. Prove that Kahn succeeds on every DAG.

**Answer:**  
Every finite DAG has a zero-indegree node. Remove one zero-indegree node and its outgoing edges. Removing nodes and edges cannot create a cycle, so the remaining graph is still a DAG. Therefore the remaining graph again has a zero-indegree node unless empty. Repeating this processes every node.

## Q22. Why does queue exhaustion with remaining nodes guarantee a cycle?

**Answer:**  
Every remaining node has positive indegree. Choose any remaining node and repeatedly follow an incoming edge. Since there are finitely many nodes, eventually one repeats. The repeated segment forms a directed cycle.

## Q23. Could reversing every edge still detect cycles?

**Answer:**  
Yes, cycle existence is preserved under reversing all edges. However, the natural course representation is prerequisite -> course because indegree then has the intuitive meaning of unresolved prerequisites.

## Q24. How would you return an actual cycle?

**Answer:**  
DFS is convenient. Keep parent pointers and the current recursion stack. When you encounter a visiting node, follow parents backward until reaching that ancestor to reconstruct the cycle.

## Q25. How can you tell whether the topological ordering is unique?

**Answer:**  
During Kahn's Algorithm, if the queue ever contains more than one node, there is a choice and therefore more than one possible topological order. A unique order requires queue size 1 at every step.

## Q26. How would you find the minimum number of semesters if unlimited courses can be taken in parallel?

**Answer:**  
Process Kahn's queue level by level. All nodes currently in the queue belong to the same semester. Increment a semester counter after processing each level.

## Q27. What changes if at most `k` courses can be taken per semester?

**Answer:**  
Simple greedy Kahn levels may not be optimal. The problem may require bitmask DP or state-space search depending on constraints because we must choose which available courses to take.

## Q28. What if courses have durations?

**Answer:**  
Use topological ordering plus dynamic programming. Earliest finish time for a course is:

```text
duration[course] + max(finish_time[prerequisite])
```

over all prerequisites.

## Q29. What if prerequisite edges are added dynamically?

**Answer:**  
Re-running topological sort is the simple solution, but advanced systems use dynamic topological-order maintenance to update the ordering efficiently.

## Q30. How would you count all valid course orders?

**Answer:**  
This is much harder than finding one. For small `n`, use bitmask DP where each state represents the set of courses already completed, and transition only to currently available courses.

## Q31. Could strongly connected components solve this problem?

**Answer:**  
Yes. A directed graph contains a cycle if an SCC has more than one node, or one node with a self-loop. Tarjan's or Kosaraju's algorithm can detect this, but they are more complex than needed here.

## Q32. Why is the complexity `O(V+E)` instead of `O(VE)`?

**Answer:**  
Every node is queued and processed at most once. Each directed edge is examined once when its source node is processed. Work is summed over all nodes and edges, not repeated for every node.

## Q33. What happens if duplicate prerequisite pairs exist?

**Answer:**  
If duplicates are treated literally, each duplicate increments indegree and appears in the adjacency list, so decrements remain balanced. If duplicates are semantically redundant, deduplicate edges first.

## Q34. How does Kahn relate to build systems?

**Answer:**  
A build target can run only when all dependencies are complete. Indegree is unresolved dependency count; zero-indegree targets are ready to build.

## Q35. How does Kahn relate to package managers?

**Answer:**  
Packages depend on other packages. A topological ordering gives a valid installation sequence. Circular dependencies appear as cycles.

## Q36. Can Kahn be parallelized?

**Answer:**  
Conceptually yes. All zero-indegree nodes at the same stage can run in parallel. Shared indegree updates require synchronization in a concurrent implementation.

## Q37. What invariant does Kahn maintain?

**Answer:**  
Every node in the queue has zero remaining indegree, meaning every prerequisite of that node has already been satisfied.

## Q38. What invariant does three-state DFS maintain?

**Answer:**  
Every node with `state == 1` lies on the current recursion path. Reaching such a node again proves a directed cycle.

## Q39. Is topological sorting defined for undirected graphs?

**Answer:**  
No. Topological ordering relies on directional "before/after" relationships and is defined for DAGs.

## Q40. Can a single-node graph contain a cycle?

**Answer:**  
Yes, if it contains a self-loop:

```text
0 -> 0
```

Otherwise a single isolated node is acyclic.

---

# 28. Product-Company Style Follow-Ups

A common interview progression is:

### Follow-up 1

> Return one valid order.

Use Course Schedule II logic.

### Follow-up 2

> Return the smallest valid order.

Use a min-heap.

### Follow-up 3

> How many semesters if independent courses run in parallel?

Use Kahn level-order processing.

### Follow-up 4

> Each course has a duration. Find minimum total completion time.

Use topological DP.

### Follow-up 5

> Is the ordering unique?

Check whether more than one zero-indegree node is available at any step.

### Follow-up 6

> Return one actual cycle.

DFS + parent reconstruction.

### Follow-up 7

> Count all possible valid schedules.

For small graphs, consider bitmask DP.

These variations test whether you understand dependency graphs rather than one memorized implementation.

---

# 29. Similar LeetCode Problems

## LeetCode 210 — Course Schedule II

Return a valid topological order.

## LeetCode 1136 — Parallel Courses

Kahn's Algorithm plus BFS levels.

## LeetCode 2050 — Parallel Courses III

Topological sorting plus DAG dynamic programming.

## LeetCode 1462 — Course Schedule IV

Prerequisite reachability queries.

## LeetCode 802 — Find Eventual Safe States

Directed cycle reasoning.

## LeetCode 269 — Alien Dictionary

Infer character ordering using topological sort.

## LeetCode 444 — Sequence Reconstruction

Topological sorting plus uniqueness.

## LeetCode 1203 — Sort Items by Groups Respecting Dependencies

Advanced multi-level topological sorting.

---

# 30. Non-LeetCode Exercises

## Exercise 1 — Software Build Order

Targets:

```text
A, B, C, D
```

Dependencies:

```text
B requires A
C requires A
D requires B
D requires C
```

Test:

```python
targets = 4

dependencies = [
    [1, 0],
    [2, 0],
    [3, 1],
    [3, 2]
]
```

Expected:

```python
True
```

---

## Exercise 2 — Circular Package Dependency

```text
A depends on B
B depends on C
C depends on A
```

Test:

```python
packages = 3

dependencies = [
    [0, 1],
    [1, 2],
    [2, 0]
]
```

Expected:

```python
False
```

---

## Exercise 3 — Factory Assembly

```text
Frame before Engine
Engine before Car
Wheels before Car
```

Test:

```python
tasks = 4

dependencies = [
    [1, 0],
    [3, 1],
    [3, 2]
]
```

Expected:

```python
True
```

---

## Exercise 4 — Microservice Deployment

```text
Database before API
Database before Worker
API before Frontend
```

Return one valid startup order.

This is a direct Course Schedule II variant.

---

## Exercise 5 — Parallel Job Rounds

```python
jobs = 4

dependencies = [
    [1, 0],
    [2, 0],
    [3, 1],
    [3, 2]
]
```

Expected minimum rounds:

```text
3
```

One valid grouping:

```text
Round 1: 0
Round 2: 1, 2
Round 3: 3
```

---

## Exercise 6 — Weighted Job Durations

Dependencies:

```text
0 -> 1
0 -> 2
1 -> 3
2 -> 3
```

Durations:

```python
duration = [3, 4, 2, 5]
```

Find minimum total completion time assuming independent tasks can run in parallel.

Hint:

```text
Topological Sort + Dynamic Programming
```

---

# 31. Extra Practice

## Easy

1. Return all courses initially available.
2. Return the number of initially available courses.
3. Detect whether a self-loop exists.
4. Return the number of courses processed before getting stuck.
5. Return all courses still blocked after Kahn terminates.

## Medium

1. Return one valid order.
2. Return the lexicographically smallest valid order.
3. Determine whether the order is unique.
4. Return the minimum number of semesters.
5. Return one directed cycle.

## Hard

1. Count all valid topological orders.
2. Limit each semester to at most `k` courses.
3. Add course durations and compute earliest finish times.
4. Support dynamic prerequisite insertions.
5. Find a minimum set of edges whose removal makes the graph acyclic.

---

# 32. Recognition Checklist

When reading a new problem, ask:

### Are there dependencies?

```text
A must happen before B
X depends on Y
Package P requires Q
```

Think:

```text
directed graph
```

### Does it ask whether everything can be completed?

Think:

```text
cycle detection
```

### Does it ask for a valid ordering?

Think:

```text
topological sort
```

### Does it ask what can happen now?

Think:

```text
indegree == 0
```

### Does it ask for minimum parallel rounds?

Think:

```text
Kahn BFS by levels
```

---

# 33. Reconstruct Kahn Without Memorizing It

If you forget the algorithm in an interview, ask four questions.

### What tells me whether a course is blocked?

```python
indegree
```

### When I finish a course, who might become available?

```python
graph[course]
```

### Where do I keep currently available courses?

```python
queue
```

### How do I know whether the whole schedule succeeded?

```python
completed == numCourses
```

That reconstructs every major data structure.

---

# 34. Reusable Kahn Template

```python
from collections import deque


graph = [[] for _ in range(n)]
indegree = [0] * n


for u, v in edges:

    graph[u].append(v)

    indegree[v] += 1


queue = deque()


for node in range(n):

    if indegree[node] == 0:
        queue.append(node)


processed = 0


while queue:

    node = queue.popleft()

    processed += 1

    for neighbor in graph[node]:

        indegree[neighbor] -= 1

        if indegree[neighbor] == 0:
            queue.append(neighbor)


has_cycle = processed != n
```

For Course Schedule, remember:

```text
input = [course, prerequisite]
edge = prerequisite -> course
```

---

# 35. Reusable DFS Template

```python
state = [0] * n


def dfs(node):

    if state[node] == 1:
        return False

    if state[node] == 2:
        return True

    state[node] = 1

    for neighbor in graph[node]:

        if not dfs(neighbor):
            return False

    state[node] = 2

    return True
```

---

# 36. Final Interview-Ready Explanation

> I model each course as a node in a directed graph. For a prerequisite pair `[course, prerequisite]`, I add the edge `prerequisite -> course`.
>
> I use Kahn's Algorithm for topological sorting. I compute the indegree of each course, where indegree represents its number of remaining unmet prerequisites. Every zero-indegree course is initially available and goes into a queue.
>
> I repeatedly remove one available course, count it as completed, and decrement the indegree of every course that depends on it. If a dependent course reaches indegree zero, all its prerequisites are satisfied, so I add it to the queue.
>
> If I eventually process exactly `numCourses` nodes, the graph is acyclic and all courses can be finished. If the queue becomes empty before that, the remaining nodes are trapped in a dependency cycle.
>
> The time complexity is `O(V + E)` and the auxiliary space is `O(V + E)`.

---

# 37. Final Memory Summary

The entire Kahn algorithm can be remembered as:

```text
Block -> Ready -> Finish -> Unlock -> Repeat
```

or:

```text
COUNT blockers
QUEUE zero-blocker tasks
DO one task
UNLOCK dependents
CHECK whether everything finished
```

And the conceptual identity is:

```text
Course Schedule
=
Directed Graph
+
Cycle Detection
=
Topological Sort
```

The most important translation is:

```text
indegree = number of blockers still remaining
queue = currently unlocked courses
graph[x] = who is waiting for x
```

Once those meanings are clear, the code is mostly bookkeeping rather than memorization.
