import math
def calculate(n):
    line = list()
    for i in range(n+1):
        coefficient = (math.factorial(n))/(math.factorial(n-i)*math.factorial(i))
        line.append(coefficient)
    return line

print(calculate(5))
