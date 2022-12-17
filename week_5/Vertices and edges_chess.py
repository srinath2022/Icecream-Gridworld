import numpy as np
import matplotlib.pyplot as plt

width = 8
length = 8
initial_state = [1,1]

vertices = []
movements = [[2, -1],[1, -2], [-1,-2], [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1]]

for w in range(width):
    for l in range(length):
        vertices.append([(w + 1),(l + 1)])

edges = []
for state in vertices:
    for move in movements:
        if (1 <= (state[0] + move[0]) <= width) and ( 1 <= (state[1] + move[1]) <= length):
            edges.append([state, [(state[0] + move[0]), (state[1] + move[1])]])

state_touched = []
path = {}

def BFS(init_state):
    current_state = init_state
    path_number = 1
    for edge in edges:
        if (current_state == edge[0]) and (current_state not in state_touched):
            state_touched.append[current_state]
            next_state = edge[1]
            path["path number " + str(path_number)] = []
            
            
