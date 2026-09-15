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