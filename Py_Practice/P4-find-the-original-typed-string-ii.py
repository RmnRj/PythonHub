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

    
    def __characterCounter(self):
        m = 0
        temp = None
        count = 0
        self.__n = []
        self.__ExtractedText = []
        for char in self.__word:
            if temp != char:
                if temp is not None:
                    self.__n.append(count)
                    self.__ExtractedText.append(temp)
                temp = char
                count = 1
                m += 1
            else:
                count += 1
        if temp is not None:
            self.__n.append(count)
            self.__ExtractedText.append(temp)
        return m
        # m is the number of unique characters in the word

    def solver(self):

        m = self.__characterCounter()
        n = self.__n
        k = self.__k
        MOD = 10**9 + 7 # Modulo for large numbers set limit of the result.
        maxlen = sum(n)
        # DP for count
        dp = [0] * (maxlen + 1)
        dp[0] = 1
        for idx in range(m):
            cnt = n[idx]
            ndp = [0] * (maxlen + 1)
            for l in range(maxlen + 1):
                if dp[l]:
                    for take in range(1, cnt + 1):
                        if l + take <= maxlen:
                            ndp[l + take] = (ndp[l + take] + dp[l]) % MOD
            dp = ndp
        ans = 0
        for l in range(k, maxlen + 1):
            ans = (ans + dp[l]) % MOD
        print(ans)

        # Generate all possible original strings of length at least k
        results = []
        def backtrack(idx, curr, currlen):
            if idx == m:
                if currlen >= k:
                    results.append(''.join(curr))
                return
            for take in range(1, n[idx]+1):
                backtrack(idx+1, curr + [self.__ExtractedText[idx]*take], currlen+take)

        backtrack(0, [], 0)
        print("Possible outcomes:")
        for s in sorted(results, reverse=True):
            print(s)

soln = Solution("aaabbb", 3)
soln.solver()
