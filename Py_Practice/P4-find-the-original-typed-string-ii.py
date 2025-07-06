'''
Alice is attempting to type a specific string on her computer. However, she tends to be clumsy and may press a key for too long, resulting in a character being typed multiple times. You are given a string word, which represents the final output displayed on Alice's screen. You are also given a positive integer k. Return the total number of possible original strings that Alice might have intended to type, if she was trying to type a string of size at least k. Since the answer may be very large, return it modulo 10^9 + 7.

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
The possible strings are: "aab", "abb", "aaab", "aabb", "abbb", "aaabb", "aabbb" and "aaabbb". 
############################################
Why Use Modulo 
10^9+7?
This number—1,000,000,007—is used because:

**It’s a large prime number, which helps in mathematical operations like modular inverse.
**It prevents overflow when numbers get huge (like in combinatorics or dynamic programming).
**It keeps results within a manageable range (like fitting inside a 32-bit or 64-bit integer).
###########################################
'''

class Solution:
    __ExtractedText = ["",""]
    def Solution(self, word, k):
        self.__word = word
        self.__k = k
    
    def __seperator(self):
        self.__i = 0 
        temp = self.__word[0]
        for char in self.__word:
            if temp != char:
                self.__i += 1
                temp = char
            self.__ExtractedText[self.__i] += char
    
    def __arranger(self):
        self._counter = 0
        for chars in self.__ExtractedText:
            for i in chars:
                #incomplete
                x = 0
