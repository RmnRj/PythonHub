'''
P4.1
To solve P04, at we have to print this pattern like this for m line, n number.[Recomended 1st pattern]
    3   3   3                      1   1   1
    2   3   3                      0   1   1
    1   3   3                      1   0   1
    3   2   3                      0   0   1
    2   2   3  more like binary    1   1   0  but in decimal.
    1   2   1  but in reverse      0   1   0
    3   1   3                      1   0   0
    2   1   3                      0   0   0
    1   1   3
    3   3   2
    2   3   2
    1   2   2
    3   1   2
    .
    .
    .
    1   1   1
'''
m = 2 # Vertical line
n = 4 # max value for each element of vertical line 
x = [0,0,0,0,0]
for i in range(m):
    x[i] = n

count = n**m
print(f" No of horizntal line: {count}")
for i in range(count): # 2^m
   
    for j in range(m): # for reverse range(m-1, n, -1) means [ m-1 to n+1, and gap]
        
        if i == 0: # first horizontal line 
            print(f"{x[j]}", end="  ")

        elif i > 0: # 2nd horizontal line to end
            if j == 0: # 1st element vertically
                x[j] -= 1 
            
            if x[j] < 1: # subtract limiting t0 1
                    x[j] = n
                    x[j+1] -= 1
            
            print(f"{x[j]}", end="  ") # manage gap in same line

    print() # change line