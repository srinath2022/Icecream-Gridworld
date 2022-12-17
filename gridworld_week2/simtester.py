import simulator
from drawmaze import drawmaze
from genP import statespace

maze = [[0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]]

s = []
for y in range(len(maze)):
    for x in range(len(maze[0])):
        s.append((x, y))

a = ['l', 'r', 'u', 'd', 'x']

p = statespace()

so = (2, 4)

g = simulator.GridSim(s, a, p, so)

#starting location of the robot
rloc = so;
while True:
    curmaze = maze
    curmaze.reverse()
    curmaze[rloc[1]][rloc[0]] = 2
    drawmaze(curmaze)

    moves = ['l', 'r', 'u', 'd', 'x']
    move = input('Please enter a action for the robot (l,r,u,d,x):')
    if move in moves:
        action = a[moves.index(move)]
    else:
        print('Invalid action')
        continue
    rloc = g.next_state(action)

