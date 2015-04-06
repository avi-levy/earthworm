from random import SystemRandom
import sys

one = '\033[0;36m1\033[0m'
zero = '\033[0;31m0\033[0m'
blank = '\033[0;37m_\033[0m'

cont = True

while cont:
    width = int(raw_input('Enter width of rectangle: ').split()[0])
    if not width:
        continue
    height = int(raw_input('Enter height of rectangle: ').split()[0])
    if not height:
        continue

    def arrayPrint(A):
        for i,row in enumerate(A):
            for val in row:
                print one if val else zero,
            print

    r = SystemRandom()

    percolation = [[r.randint(0,1) for i in range(width)] for j in range(height)]

    arrayPrint(percolation)

    cont = (raw_input('Again? [y/n]: ') == 'y')