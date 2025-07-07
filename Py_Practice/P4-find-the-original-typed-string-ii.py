'''
Alice is attempting to type a specific string on her computer. However, she tends to be clumsy and may press a key for too long, resulting in a character being typed multiple times.
You are given a string word, which represents the final output displayed on Alice's screen. You are also given a positive integer k.
Return the total number of possible original strings that Alice might have intended to type, if she was trying to type a string of size at least k.
Since the answer may be very large, return it modulo 109 + 7.

Example 1:
Input: word = "aabbccdd", k = 7
Output: 5
Explanation:
The possible strings are: "aabbccdd", "aabbccd", "aabbcdd", "aabccdd", and "abbccdd".

Example 2:
Input: word = "aabbccdd", k = 8
Output: 1
Explanation:
The only possible string is "aabbccdd".

Example 3:
Input: word = "aaabbb", k = 3
Output: 8
'''

class Solution:
    
    def __init__(self, word, k):
        self.__word = word
        self.__k = k
        self.__ExtractedText = []
        self.__result = [] #Vertical line
        self.__n = [] # T find length of each individual charaters 

    
    def __seperator(self):
        m = 0
        i = -1
        temp = ""
        text = ""
        for char in self.__word:
            if temp != char:  # change character
                temp = char
                self.__ExtractedText.append(text) # append in list
                #text = ""
                i += 1
                self.__n[i] = 0 
                m += 1
            self.__n[i] += 1 # count no of single character repeated Ex. text = "aaaa" then n[] = 4
        self.__ExtractedText.append(text)
        return m
    

    def __addResult(self, n,m):
        for i in range(m):
            for values in self.__ExtractedText[i]:
                x = 0 ######################################## Here ################


    def solver(self):
        m = self.__seperator()
        N = 0
        n = self.__n
        N = 1
        for values in n:
            N *= values # used to find how many possible results

        for i in range(N):
            for j in range(m):
                if i == 0:
                    n[j] = 0

        # print(self.__V)
        # for values in self.__ExtractedText:
        #     print(values)

soln = Solution("aaabbbccc", 5)
soln.solver()
