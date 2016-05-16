"""
Daniel J. Rothblatt's Cellular Automaton
WHAT THIS PROGRAM CAN DO:
    -Generate an n x n cellular automaton
    -Step through rule applications (or not)

WHAT NEEDS TO BE DONE:
    -Make a non-cmdline version: I should be able to turn cells on 
    at the beginning with my mouse and all that good stuff
    -(?) Create a cmdline way of starting out with some cells on, 
    if this can be done without being tedious
    -Perhaps real-valued entries rather than binary values?
        -Good visualization VERY necessary for this!
        -What are the rules like when you do this?
"""

from sys import argv
"""
Step zero: Specify your rules and get cmdline arguments
"""

# position i as a binary number reflects the configuration, value tells you how to change
# e.g., spot 5 = 101 = cell off, both neighbors on
#        0  1  2  3  4  5  6  7
RULES_1D = [0, 0, 0, 0, 1, 1, 0, 1]

#row i tells you what to do if your current entry == i (i in {0, 1})
#column j tells you what to set your current entry to if j neighbors == 1
#    0  1  2  3  4  5  6  7  8
RULES_2D = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0]
]

N = 100
SPILL = False
DIMENSION = 2
NUM_ITERATIONS = 10
CONTROL = False
for i in range(len(argv)):
    arg = argv[i]
    if arg == "-n":
        N = int(argv[i+1])
    elif arg == "-s":
        SPILL = True
    elif arg == "-i":
        NUM_ITERATIONS = int(argv[i+1])
    elif arg == "-c":
        CONTROL = True
    elif arg == "-d":
        DIMENSION = int(argv[i+1])

"""
Step one: Build an N x N binary matrix with entries initialized to 0
"""

def init_matrix(N):
    M = [[0 for i in range(N)] for j in range(N)]
    return M

def print_matrix(M):
    size = len(M)
    out = ""
    for i in range(size):
        for j in range(size):
            # out += str(M[i][j]) + " " 
            if M[i][j]:
                out += u"\u2588"
            else:
                out += " "
        out += "\n"
    print(out)

'''
Step two: Count how many neighbors of your current cell are 1 
cur_M: matrix
i: nat
j: nat
spill: bool
dim: nat

i, j gives us row, column of cur_M, respectively
spill tells us whether we are looking at a box or a sphere
(the difference: In a box, when you are at the edge, there's nowhere to go;
in a sphere, when you're at the edge, there is no edge, you come out the other side)
'''

def count_neighbors(cur_M, i, j, spill, dim):
    def row_count(M, i, j):
        count = 0
        if look_l: # can we look left?
            count += M[i][j-1]
        elif spill:
            count += M[i][end_pos]
        
        count += M[i][j]
        
        if look_r: # can we look right?
            count += M[i][j+1]
        elif spill:
            count += M[i][0]
        return count 

    def row_count_1D(M, i, j): # in 1D, we construct binary numbers to choose rules
        count = 0
        if look_l: 
            count |= M[i][j-1] << 2 # highest bit is the left
        elif spill:
            count |= M[i][end_pos] << 2

        count |= M[i][j] << 1 # second bit is the cell itself

        if look_r: 
            count |= M[i][j+1] # lowest bit is the right
        elif spill:
            count |= M[i][0]
        return count 

    count = 0
    end_pos = len(cur_M) - 1
    look_u = i > 0 #if look_u: we can look up because we're not in row 0
    look_d = i < end_pos #if look_d: we can look down because we're not in row N
    look_l = j > 0 #if look_l: we can look left because we're not in column 0
    look_r = j < end_pos #if look_r: we can look right because we're not in column N

    if dim == 1:
        count = row_count_1D(cur_M, i, j)

    #count row above
    if dim > 1:
        if look_u:
            count += row_count(cur_M, i-1, j)
        elif spill: #we CAN'T look up, but can we look at the bottom?
            count += row_count(cur_M, end_pos, j)
        #count row below
        if look_d:
            count += row_count(cur_M, i+1, j)
        elif spill:
            count += row_count(cur_M, 0, j)
        #count row we're at
        count += row_count(cur_M, i, j) - cur_M[i][j] #not counting self...
    #DONE!

    return count

'''
Step three: Change all entries of matrix based on number of neighbors that are on or off
'''
def apply_rules(cur_M):
    size = len(cur_M)
    next_M = init_matrix(size)
    for i in range(size):
        for j in range(size):
            if DIMENSION == 1:
                count = count_neighbors(cur_M, i, j, SPILL, 1)
                next_M[i][j] = RULES_1D[count]
            if DIMENSION > 1:
                entry = cur_M[i][j] #will be either 0 or 1, so we grab row with it
                count = count_neighbors(cur_M, i, j, SPILL, DIMENSION)
                next_M[i][j] = RULES_2D[entry][count]
    return next_M

cur_matrix, next_matrix = init_matrix(N), init_matrix(N)
print("Our initial matrix:")
print_matrix(cur_matrix)

for i in range(NUM_ITERATIONS):
    if CONTROL:
        stop = input("Hit enter to advance to step %d,\nOR type 'stop' or 's' to break out early\n" %(i+1))
        if stop in ["stop", "s"]:
            print("Terminating...")
            break
    cur_matrix = list(apply_rules(cur_matrix))
    print("iteration %d:" %(i+1))
    print_matrix(cur_matrix)
