from math import comb

class Solution:
    def numberOfWays(self, startPos: int, endPos:int, k:int) -> int:
        modulo = 10**9 + 7

        distance = endPos - startPos

        if distance > k:
            return 0
        
        if (k - distance) % 2 != 0:
            return 0

        right = (distance + k) //2 

        return comb(k, right) % modulo


solution = Solution()

startPos = 2
endPos = 5
k = 111

answer = solution.numberOfWays(startPos, endPos, k)

print(answer)