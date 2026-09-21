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

            # Node is already on current recursion path.
            if state[course] == 1:
                return False

            # Completely processed previously.
            if state[course] == 2:
                return True

            # Enter recursion path.
            state[course] = 1

            for next_course in graph[course]:

                if not dfs(next_course):
                    return False

            # Remove from recursion path;
            # mark completely processed.
            state[course] = 2

            return True

        for course in range(numCourses):

            if state[course] == 0:

                if not dfs(course):
                    return False

        return True



solution = Solution()

numCourses = 4

prerequisites = [
    [1,0],
    [2,0],
    [3,1],
    [3,2]
]

answer = solution.canFinish(numCourses, prerequisites)


print(answer)