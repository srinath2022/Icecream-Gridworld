import numpy as np
import matplotlib.pyplot as plt
import copy

width = 8
length = 8
initial_state = [1,1]

reward_state = [2,1]

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
path = []

def BFS(init_state, path, state_touched):
    next_level_path = copy.deepcopy(path)
    if len(path) == 0:
        path.append(init_state)
        state_touched.append(init_state)
    for current_path in path:
        if len(path) == 1:
            current_state = current_path
        else:
            current_state = current_path[-1]
        for edge in edges:       
            if (current_state == edge[0]) and (edge[1] not in state_touched):
                next_state = edge[1]
                state_touched.append(next_state)
                path_to_add = []
                for spot in current_path:
                    path_to_add.append(spot)
                path_to_add.append(next_state)
                next_level_path.append(path_to_add) 
                if next_state == reward_state: 
                    print("found a solution path" + str(next_level_path[-1]))
                    return
    if next_level_path == path:
        print("There was no found solution")
        print("States touched : " + str(state_touched))
        print(len(state_touched))
    else:
        BFS(initial_state, next_level_path, state_touched)

BFS(initial_state, path, state_touched)
            
