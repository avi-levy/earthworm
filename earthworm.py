from random import SystemRandom
from sys import stdin
# from time import sleep

one = '\033[0;36m1\033[0m'
zero = '\033[0;31m0\033[0m'

blank = '\033[0;37m_\033[0m'
aster = '\033[0;37m*\033[0m'

r = SystemRandom()

def arrayPrint(worm, start, end):
    """
        print the sand from start to end
    """
    A, cur = worm
    for i in range(start[0], end[0]):
        for j in range(start[1], end[1]):
            if cur == [i,j]:
                print aster,
            else:
                print one if A[i][j] else zero,
        print

def push(worm, dim, move):
    """
        worm = (A, cur) where:
            cur is the location of the earthworm
            A is the matrix of sand
        dim: dimensions of the matrix
        move: move to apply to the earthworm

        Returns false if and only if the earthworm hit the boundary
    """
    if not move:
        return True

    dir, d = move
    A, cur = worm

    # make a hole
    A[cur[0]][cur[1]] = 0

    # update current location
    cur[d] += dir
    
    # don't push if we are at the boundary
    bound = dim[d] if dir == 1 else -1
    if dir*(cur[d] - bound) >= 0:
        cur[d] -= dir
        return False

    if d is 0:
        spot = lambda a: (a, cur[1])
    else:
        spot = lambda a: (cur[0], a)

    # look for first 0 along direction of motion
    for j in range(cur[d], bound, dir):
        x,y = spot(j)

        if A[x][y] is 0:
            # print "Found 0 after ", j, " steps"

            # push the sand over
            for k in range(j, cur[d], -dir):
                toX, toY = spot(k)
                fromX, fromY = spot(k - dir)
                A[toX][toY] = A[fromX][fromY]

            return True

    # there is no hole to push sand into
    return True

def promptMove():
    key = raw_input()
    if not key:
        return
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
        return
    return dir, slope

def randomMove():
    return r.sample([-1,1],1)[0], r.randint(0,1)

def promptDim(name, h, w):
    height = raw_input('Enter height of %s (default %s): ' % (name,h) )
    if not height:
        height = h
    else:
        height = int(height.split()[0])

    width = raw_input('Enter width of %s (default %s): ' % (name,w) )
    if not width:
        width = w
    else:
        width = int(width.split()[0])

    return height, width

def initialize(dim):
    # Random initial configuration:
    # [[r.randint(0,1) for i in range(dim[0])] for j in range(dim[1])]
    return (
            [[1 for i in range(dim[1])] for j in range(dim[0])],
            [dim[0]/2, dim[1]/2]
        )

def showEarthworm(worm, dim, view):
    arrayDimS = (
            (dim[0] - view[0])/2,
            (dim[1] - view[1])/2
        )

    arrayDimE = (
            (dim[0] + view[0])/2,
            (dim[1] + view[1])/2
        )
    arrayPrint(worm, arrayDimS, arrayDimE)

def runRandom(dim, view, steps):
    worm = initialize(dim)

    hitBoundary = False

    for x in range(steps):
        if not push(worm, dim, randomMove()):
            hitBoundary = True

    showEarthworm(worm, dim, view)

    total = 0
    for row in worm[0]:
        for val in row:
            if not val:
                total += 1
    print "Number of holes: ", total
    print "Hit the boundary: ", hitBoundary

def runTrials(dim, view, steps, trials):
    totals = []
    for x in range(trials):
        worm = initialize(dim)

        for x in range(steps):
            if not push(worm, dim, randomMove()):
                print "Trials invalidated, hit the boundary at iteration ", x, "/", steps
                return False

        total = 0
        for row in worm[0]:
            for val in row:
                if not val:
                    total += 1
        print "Number of holes: ", total
        totals.append(total)
    print "Mean: ", sum(totals)/trials
        

def runHuman(dim, view):
    worm = initialize(dim)

    key = True
    while key:
        showEarthworm(worm, dim, view)
        key = promptMove()
        push(worm, dim, key)

while True:
    print "Earthworm Simulation (c) 2015 Avi Levy"

    dim = promptDim('bounding box', 1000, 1000)
    view = promptDim('viewport', 60, 80)

    if raw_input('Interactive? [y/n]: ') == 'y':
        print "Use w/a/s/d to move up/left/down/right and type q to quit."
        runHuman(dim, view)

    else:
        steps = int(raw_input('Number of steps: '))

        trials = raw_input('Number of trials: ')
        if not trials:
            trials = 0
        trials = int(trials.split()[0])
        if trials <= 1:
            runRandom(dim, view, steps)
        else:
            runTrials(dim, view, steps, trials)

    if raw_input('Run again? [y/n]: ') != 'y':
        break