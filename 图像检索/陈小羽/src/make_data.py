import random as rand

sz = rand.randint(1000, 1000)
print(sz)
n = rand.randint(1000, 1000)
print(n)

def genALine():
    lst = [rand.randint(-1000, 1000) for i in range(sz)]
    for i in lst:
        print(i, end = ' ')
    print('')


for t in range(n):
    genALine()

genALine()
