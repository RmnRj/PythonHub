# Optimized way. This is done through mathematical eqn

# Let,
# A = Actual Sum of 1 to N  ||    C = Calculated Sum of given array
# M = Missing number        ||    D = Duplicate Number
# AA = sum of sq of number  ||    CC = Calculated sum of sq of given number

#   Now,
#       A - C = M - D = X (SAY) ------------ eqn 1
#       M + D = Y (SAY) --------------------eqn 2
#     AA - CC = M^2 - D^2 = Z (SAY)   ------- eqn 3    
   
# Then, 
#     M^2 - D^2   = (M - D)(M + D)
# or, M^2 - D^2   = X * Y
#      Y = (Z)/X --------------------- eqn 3

# Finally,
#   M - D + M + D = X + Y
#   2M = X + Z/X -------------- RESULT
#   D = M - X ----------------- RESULT

print("\n\n###############################################################################\n")
print("Optimized Version using mathematics")
print("Run this program multiple times and found time to complete is normally")
print("less than 0.2 second to check 1 to 100000") 
print("\n###############################################################################\n\n")


def Finder(nums):
    n = len(nums)

    # if representation is taken from above solved expresson
    A = n * (n + 1) // 2
    AA = n * (n + 1) * (2 * n + 1) // 6

    C = sum(nums)
    CC = sum( i * i for i in nums)

    X = A - C

    missing =  (X + (AA - CC) // X) // 2

    duplicate = missing - X                               

    return [duplicate, missing]

print(f"Input: [1, 5, 6, 4, 4, 7, 3, 9]\nOutput: {Finder([1, 2, 5, 6, 4, 4, 7, 3, 9])}")

nums = list(range(1, 100001)) # 1 to 150
nums.remove(222) # remove from list
nums.append(7777) # append in list

print(f"\nOutput: {Finder(nums)}")