from random import SystemRandom
import sys
from sys import stdin

one = '\033[0;36m1\033[0m'
zero = '\033[0;31m0\033[0m'

blank = '\033[0;37m_\033[0m'
aster = '\033[0;37m*\033[0m'

def arrayPrint(cur, A):
    for i,row in enumerate(A):
        for j,val in enumerate(row):
            if cur == [i,j]:
                print aster,
            else:
                print one if val else zero,
        print

def push(dir, d):
    # make a hole
    A[cur[0]][cur[1]] = 0

    # update current location
    cur[d] += dir

    if dir == 1:
        bound = dim[d]
        if cur[d] >= bound:
            # don't push - we are at boundary
            cur[d] -= dir
            return
    elif dir == -1:
        bound = -1
        if cur[d] <= bound:
            cur[d] -= dir
            # don't push - we are at boundary
            return

    for j in range(cur[d], bound, dir):
        if d is 0:
            if A[j][cur[1]] is 0:
                # print "hit a 0 at ", j
                for k in range(j, cur[d], -dir):
                    # print "copying ", k-dir, " to ", k
                    A[k][cur[1]] = A[k - dir][cur[1]]
                break            
        elif d is 1:
            if A[cur[0]][j] is 0:
                # print "hit a 0 at ", j
                for k in range(j, cur[d], -dir):
                    # print k
                    A[cur[0]][k] = A[cur[0]][k - dir]
                break            

while True:
    print "============="
    dim = [0, 0]
    dim[0] = int(raw_input('Enter height of rectangle: ').split()[0])
    if not dim[0]:
        continue
    dim[1] = int(raw_input('Enter width of rectangle: ').split()[0])
    if not dim[1]:
        continue

    #r = SystemRandom()
    #A = [[r.randint(0,1) for i in range(dim[0])] for j in range(dim[1])]
    A = [[1 for i in range(dim[1])] for j in range(dim[0])]
    cur = [dim[0]-1, dim[1]/2]
    
    key = None
    while key is not 'q':
        arrayPrint(cur, A)
        print

        key = raw_input()
        if not key:
            continue
        key = key[0]

        if key == 'a':
            dir, slope = -1, 1
        elif key == 'd':
            dir, slope = 1, 1
        elif key == 's':
            dir, slope = 1, 0
        elif key == 'w':
            dir, slope = -1, 0
        else:
            continue
        push(dir, slope)
