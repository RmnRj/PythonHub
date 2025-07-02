'''You are given an array nums containing n integers. This array originally contained all integers
 from 1 to n exactly once. Due to a data error, one number in the original sequence from 1 to n is
 duplicated (it appears twice), and another number is missing (it is not present at all). All other
 numbers appear exactly once.

Your task is to find the duplicated number and the missing number. {1-9} nums = [1, 5, 6, 4, 4, 7, 3, 9]

Example:
Input: nums = [1, 2, 2, 4]
Expected Output: [2, 3] (2 is the duplicate, 3 is the missing number)

Answer is [4,8]'''

# Code
# Checking each no 1 to n to each value of "nums" array and count how may times no is matched.
# Zero time match for missing number and two time match for dublicate number. 

print("\n\n###############################################################################\n")
print("Easy Version using mathematics")
print("Run this program multiple times and found it takes so so long")
print("more than 10, 20 second sometimes to check 1 to 100000")
print("\n###############################################################################\n\n")

def Finder(nums):
    n = len(nums)
    missing = 0
    duplicate = 0

    for i in range(n):
        counter = 0 
        for j in nums:
            if j == i+1:
                counter += 1
        if counter == 0:
            missing = i+1
        elif counter == 2:
            duplicate = i+1

    return [duplicate, missing]

print(f"Input: [1, 2, 5, 6, 4, 4, 7, 3, 9]\nOutput: {Finder([1, 2, 5, 6, 4, 4, 7, 3, 9])}")

nums = list(range(1, 100001)) # 1 to 150
nums.remove(222) # remove from list
nums.append(7777) # append in list

print(f"\nOutput: {Finder(nums)}")
