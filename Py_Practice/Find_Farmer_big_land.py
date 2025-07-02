'''A farmer wants to farm their land with the maximum area where good land is present.
 The “land” is represented as a matrix with 1s and 0s, where 1s mean good land and 0s 
 mean bad land. The farmer only want to farm in a square of good land with the maximum
 area. Please help the farmer to find the maximum area of the land they can farm in good
 land.

Example: Try on any programming language.

0 1 1 0 1
1 1 0 1 0
0 1 1 1 0
1 1 1 1 0
1 1 1 1 1
0 0 0 0 0
'''

# We should check smallest square to big square for good lands but we need to check to biggest square.
# Other way, we check biggest square to smallest. We need to find maximum good area of this way is best.

LandWidth = 5
LandBridth = 6

print("Finding...")

# This is to check good land
def checker(row_start, col_start, size):
    land = [
        [0, 1, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0]
    ]
    # Check if the square defined by (row_start, col_start) and size
    # is entirely within the land boundaries.
    if row_start + size > len(land) or col_start + size > len(land[0]):
        return False # Square goes out of bounds

    for r in range(row_start, row_start + size):
        for c in range(col_start, col_start + size):
            if land[r][c] == 0:
                return False  # Found a bad spot (0), so it's not a good land square
    return True  # All cells in the square are 1s


# Determine the maximum possible square size to start searching from
max_possible_size = min(LandWidth, LandBridth)
found_max_square = False
best_bp1 = -1
best_bp2 = -1
best_size = 0

# Iterate from the largest possible square size down to 1
for current_size in range(max_possible_size, 0, -1):
    if found_max_square: # If we already found the largest, no need to check smaller ones
        break
    # Iterate through all possible top-left corners (bp1, bp2)
    # The loop limits ensure the square fits within the land
    for bp2 in range(LandBridth - current_size + 1): # bp2 is row start
        for bp1 in range(LandWidth - current_size + 1): # bp1 is column start
            if checker(bp2, bp1, current_size):
                best_bp1 = bp1
                best_bp2 = bp2
                best_size = current_size
                found_max_square = True
                break # Found the largest for this size, move to next smaller size
        if found_max_square:
            break

# Final Output
if found_max_square:
    print("\nFound.")
    print(f"Location : ( {best_bp2}, {best_bp1} )")
    print(f"Size : ( {best_size}, {best_size} )") # For a square, width and height are the same

    # Print the land with the found square highlighted (conceptually, by printing 1s)
    # This loop now correctly identifies which cells are part of the found square
    for j in range(LandBridth):
        for i in range(LandWidth):
            if (i >= best_bp1 and i < best_bp1 + best_size) and \
               (j >= best_bp2 and j < best_bp2 + best_size):
                print("1", end="  ") # Part of the found square
            else:
                # You might want to print the original land value here instead of 0,
                # but based on your request, printing 0 for non-square cells.
                # For more accuracy, you'd fetch land[j][i]
                print("0", end="  ")
        print() # Newline after each row (removed "\n" for cleaner output, `print()` alone adds newline)
else:
    print("\nNot Found. There is no good land square.")