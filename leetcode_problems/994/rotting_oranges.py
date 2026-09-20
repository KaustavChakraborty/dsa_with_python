from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows= len(grid)
        cols = len(grid[0])
        
        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):
                if (grid[row][col] == 2):
                    queue.append((row, col))
                if (grid[row][col] == 1):
                    fresh += 1

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        minute = 0

        while queue and fresh > 0:
            level_size = len(queue)

            for _ in range(level_size):
                row, col = queue.popleft()
                for dr,dc in directions:
                    nr = row + dr
                    nc = col + dc

                    if (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1):
                        grid[nr][nc] = 2
                        queue.append((nr, nc))
                        fresh -=1
            minute += 1
        
        if fresh > 0:
            return -1

        return minute 




grid = [
    [2,1,1],
    [1,1,0],
    [0,1,1]
]



solution = Solution()

answer = solution.orangesRotting(grid)

print(answer)