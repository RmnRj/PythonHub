"""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

 

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints: [Rules]
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.
 
Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?"""

class Solution:
    def twoSum1(self, nums, target): # Time complexity O(n) solution [from AI]
        seen = {}  # Dictionary to store value: index
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
    
    def twoSum2(self, nums, target): # Time complexity O(n^2) solution [from myself]
        no = []
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if target == nums[i] + nums[j]:
                    no.append(i)
                    no.append(j)
                    break
        return no

# Main logic
nums = [1, 2, 3, 5, 8]
target = 11
soln = Solution()
no = soln.twoSum2(nums, target)
print(f"[{no[0]}, {no[1]}]")