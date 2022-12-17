import numpy as np

def statespace():
    # maze where open spaces are zeros and walls are ones
    maze = [[0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]]
    # actions [left, right, up, down, nothing] represented by cartesian movement
    act = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]
    # probability of error
    pe = 0.1

    # This is the full list of transition probabilities
    #   Dim 1 and 2 represent the (x,y) coord of the current state in the maze
    #   Dim 3 represents the different actions that can be taken [l, r, u, d, -]
    #   Dim 4 and 5 represent the (x,y) coord of the next state in the maze given the action taken
    widthm = len(maze[0])
    heightm = len(maze)
    tprob = np.zeros((widthm * heightm, len(act), widthm * heightm))

    # Loop through every state in the maze represented by a x,y coords
    #   For every (x,y) choose an action a and determine the probability of b actually happening
    #   Save probabilities at the appropriate location in tprob[x][y][action][x'][y']
    for y in range(heightm):
        for x in range(widthm):
            for a in act:
                # Additional probability to stay still. Used when states are impossible and get "folded in" to stay still.
                ps = 0
                for b in act:
                    if a == b:
                        p = 1 - pe
                    else:
                        p = pe / 4
                    sx = x + b[0]
                    sy = y + b[1]

                    # if the action will result in robot going out of bounds, add probability to ps, continue
                    if sx < 0 or sx > widthm-1 or sy < 0 or sy > heightm-1:
                        ps += p
                        continue
                    # if the action wll result in robot going into a wall, add probabilty to ps, continue
                    elif maze[sy][sx] == 1:
                        ps += p
                        continue
                    # else save the probability at the appropriate location tprob[x][y][action][x'][y'] give action a
                    else:
                        tprob[x+widthm*y][act.index(a)][x+b[0]+widthm*(y+b[1])] = p

                # Additional probability to stay still will be added to value at tprob[x][y][action][x'][y']
                # where x = x' and y = y'
                tprob[x+widthm*y][act.index(a)][x+widthm*y] += ps
    return tprob
