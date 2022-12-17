
import array
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

##Problem Setup inputs
#Dimensions depth of grid
x_dim = 5
y_dim = 5
#Obstacles details
obs_spot_given = True
obs_1 = [1,1]
obs_2 = [1,3]
obs_3 = [2,1]
obs_4 = [2,3]
obs_list = [obs_1, obs_2, obs_3, obs_4]
#IceCream details
ic_given = True
ic_rd = [2,2]
ic_rs = [2,0]
ic_list = [ic_rd, ic_rs]
#Initial starting spot
state_start = [2,4]
#Road Spots
road_list = []
vertical_x_cord = 4
for y in range(y_dim):
    road_list.append([vertical_x_cord, y])
#transistion probability error
prob_error = .1  

##Setup Problem with S, A, P, O definitions
#States: in this case create 2d grid map, and each block in x,y corresponds to a state 
grid = []
for x in range(x_dim):  
    for y in range(y_dim):
        state = [x,y]
        grid.append(state)
#Actions:
action_list = [ "Up", "Down", "Left", "Right", "Stay"]
action_vector = [[0,1], [0,-1], [-1, 0], [1,0], [0,0]]
#Probabilities: prob of transitions occuring (either takes directed action or equal chance divide by other actions), this is calculated based on state in and directed input action
    #Transiations: defined by (State, Action, State). All transitions are listed, even if the possibility of transition happening is zero
transition_list = []
for initial_state in grid:
    for action in action_list:
        for new_state in grid:
            transition_list.append([initial_state, action, new_state])      
    #Remove Transitions that have Zero Proabability: move off the map, start state or end state in obstacle, move more than one othogonal space or not in direction of action
transition_non_zero_prob_list = []
for transition in transition_list:
    #adding possible x dimenion movements
    if ((transition[1] == "Left") and not(transition[0][0] == 0)) or (transition[1] == "Right") and not(transition[0][0] == (x_dim-1)): 
        if transition[1] == "Right" and (transition[2] == [transition[0][0] + 1, transition[0][1]]):
           transition_non_zero_prob_list.append(transition)
        elif transition[1] == "Left" and  (transition[2] == [transition[0][0]  -1, transition[0][1]]):
            transition_non_zero_prob_list.append(transition)
    #adding possible y dimenion movements
    elif ((transition[1] == "Down") and not(transition[0][1] == 0)) or (transition[1] == "Up") and not(transition[0][1] == (y_dim-1)):
        if transition[1] == "Up" and (transition[2] == [transition[0][0]    , transition[0][1] + 1]):
            transition_non_zero_prob_list.append(transition)
        elif transition[1] == "Down"  and (transition[2] == [transition[0][0]    , transition[0][1] - 1]): 
            transition_non_zero_prob_list.append(transition)
    #adding possible stay movements
    elif transition[1] == "Stay" and  transition[0] == transition[2]:
        transition_non_zero_prob_list.append(transition)
    #removing obstacle states in initial or final state
    for obs in obs_list:
        if (transition[0] == obs) or (transition[2] == obs):
            try:
                transition_non_zero_prob_list.remove(transition)
            except:
                continue
#create a function that lists possible transitions given state
def transitions_possible(current_state):
    print("Currently on spot: " + str(current_state))
    print("The possible transitions are: ")
    possible_transitions = []
    for transition in transition_non_zero_prob_list:
        if transition[0] == current_state:
            possible_transitions.append(transition)
    print(possible_transitions)
    return(possible_transitions)  
#Create transition function that calculaties probabilities when in a state and told a given action, and produces outcome given those probabilities and barriers
def transition(current_state, input_action): #where iput action is in action verb list
    action_list_to_list = action_vector[action_list.index(input_action)]
    print("action list to list is "  + str(action_list_to_list))
    
    action_input_list = [input_action] #creating a list which has intended action first, followed by other actions to correspond to probability list
    for action in action_list:  
        if input_action != action:
            action_input_list.append(action)
    action_prob = [(1- prob_error)] #probabilities corresponding to action_input_list (starts with intended action, and had probability 1 - prob_error)
    for prob in range(len(action_vector)-1):
        action_prob.append(prob_error/(len(action_vector)-1)) #all other actions have similar chance of occuring
    decision = np.random.choice(action_input_list, p= action_prob) #the action decision will be based on probabilities and input action
    if decision == action_input_list[0]:
        print("No error from transition probability")
        possible_next_state = [(current_state[0] + action_list_to_list[0]),(current_state[1] + action_list_to_list[1])]
    else:
        print("Error from transition probability, actually trying action " + str(decision))
        action_list_to_list = action_vector[action_list.index(decision)]
        possible_next_state = [(current_state[0] + action_list_to_list[0]),(current_state[1] + action_list_to_list[1])]
    print(" possible next state is " + str(possible_next_state))
    transition_attempt = [current_state, decision, possible_next_state]
    print("transition attempt is "+ str(transition_attempt))
    if transition_attempt in transitions_possible(current_state):
        print("This transition is possible with no barrier, moving to " + str(transition_attempt[2]) + " with action " + str(input_action))
        next_state = transition_attempt[2]
        observation(next_state)
        return next_state
    else:
        print("This transition is impossible due to barriers, forced to stay in place")
        observation(current_state)
        return current_state
#Observations : proabalities of observations based on how far away icecream store and probabiltiy of observation defined 
def observation(current_state):
    dist_d = abs(ic_rd[0] - current_state[0]) + abs(ic_rd[1] - current_state[1]) #calculating distance from icecream store d
    dist_s = abs(ic_rs[0] - current_state[0]) + abs(ic_rs[1] - current_state[1]) #calculating distance from icecream store s
    print(current_state)
    if (current_state == ic_rd) or (current_state == ic_rs):
        print("got ice cream")
    else:
        h = 2/((1/dist_d) + (1/dist_s)) #compute euclidean distance
        observation_list = [math.ceil(h), math.floor(h)] #possible observations
        observation_probs = [(1- (math.ceil(h) - h)),(math.ceil(h) - h)] #probabilities corresponding possible observations
        observed_actual = np.random.choice(observation_list, p = observation_probs)
        print("Observed distance " + str(observed_actual))

def drawmaze(current_state, maze): 
    plt.axes()
    for x in range(len(maze)):
        for y in range(len(maze)):
            if maze[y][x] == 0:
                rectangle = plt.Rectangle((x, y), 1, 1, fc='white', ec="black")
                plt.gca().add_patch(rectangle)
            if maze[y][x] == 1:
                rectangle = plt.Rectangle((x, y), 1, 1, fc='gray', ec="black")
                plt.gca().add_patch(rectangle)
            if maze[y][x] == 2:
                rectangle = plt.Rectangle((x, y), 1, 1, fc='green', ec="black")
                plt.gca().add_patch(rectangle)
            if maze[y][x] == 3:
                rectangle = plt.Rectangle((x, y), 1, 1, fc='red', ec="black")
                plt.gca().add_patch(rectangle)
            if maze[y][x] == 4:
                rectangle = plt.Rectangle((x, y), 1, 1, fc='pink', ec="black")
                plt.gca().add_patch(rectangle)
    plt.axis('scaled')
    plt.draw()
    plt.pause(.2)
    next_state_taken = take_action(current_state)
    show_maze(next_state_taken)       

def show_maze(current_state):
#in maze 0 = nothing, 1 = barrier, 2 = your spot, 3 = road, 4 = ice cream
    maze = [] 
    for x in range(x_dim): 
        maze.append([])
        for y in range(y_dim):
            maze[x].append(0)
    for obs in obs_list: #add obstacles
        maze[obs[1]][obs[0]] = 1  
    for ic in ic_list: #add ice cream spots
        maze[ic[1]][ic[0]] = 4
    for road in road_list: #add obstacles
        maze[road[1]][road[0]] = 3
    try:
        maze[current_state[1]][current_state[0]] = 2 #add current spot
    except:
        pass
    
    drawmaze(current_state, maze)

def take_action(current_state):
    action_attempt = input("Enter action:")
    print("Desired input action is: ")
    if str(action_attempt) == 'u':
        print("Up")
        return transition(current_state, "Up")
    elif str(action_attempt) == 'd':
        print("Down")
        return transition(current_state, "Down")
    elif str(action_attempt) == 'l': 
        print("Left")
        return transition(current_state, "Left")
    elif str(action_attempt) == 'r':
        print("Right")
        return transition(current_state, "Right")
    elif str(action_attempt) == 's':  
        print("Stay")
        return transition(current_state, "Stay")
    elif str(action_attempt) == 'q':
        print("Quit")
        quit()  
    else:
        print("not a valid action")
        take_action(current_state)

show_maze(state_start)













        


            


