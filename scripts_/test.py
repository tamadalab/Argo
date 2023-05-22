import math
import os
import random
import re
import sys



#
# Complete the 'getOneBits' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER n as parameter.
#

def getOneBits(n):
    # Write your code here
    list = []
    l = 0
    list_a = []
    list.append(bin(n)[2:])
    a = bin(n)[2:]
    s = str(a)
    for i in range(len(s)):
        if s[i] == 1:
            list_a.append(l)
        l+=1
    return list
    
    
    
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    result = getOneBits(n)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
