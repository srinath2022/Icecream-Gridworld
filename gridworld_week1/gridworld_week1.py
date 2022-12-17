 
import array
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

#Dimensions depth of grid
x_dim = 5
y_dim = 5
#Create 2d grid map
grid = []
for x in range(x_dim):  
    for y in range(y_dim):
        state = [x,y]
        grid.append(state)
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
initial_state = [2,4]
#Road Spots
road_list = []
vertical_x_cord = 4
for y in range(y_dim):
    road_list.append([vertical_x_cord, y])

#Informational Charecterising system
#States: all possible grid areas. Note that some states, you cannot be in due to obstacles.
print("Possible states are:")
for state in grid:
    print(state)

#Actions: move up, down, left, right, or stay
action_list = [ "Up", "Down", "Left", "Right", "Stay"]
print("Possible actions are:")
for action in action_list:
    print(action)

#Transitions: defined by (State, Action, State). All transitions are listed, even if the possibility of transition happening is zero
transition_list = []
for initial_state in grid:
    for action in action_list:
        for new_state in grid:
            transition_list.append([initial_state, action, new_state])
print("The total number of transitions is " + str(len(transition_list)))
print("An example of transition is " + str(transition_list[0]))
#End informational

#Create Transition list
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
print("The total number of non-zero probability transitions is " + str(len(transition_non_zero_prob_list)))
print("Only " + str(len(transition_non_zero_prob_list)/len(transition_list) * 100) + " percent of existing transitions have non-zero probability")
print(transition_non_zero_prob_list)
#Movement Functions
def list_transitions(square):
    print("Currently on spot: " + str(square))
    print("The possible transitions are: ")
    possible_transitions = []
    for transition in transition_non_zero_prob_list:
        if transition[0] == square:
            possible_transitions.append(transition)
            print(str(transition))
    return(possible_transitions)    

def choose_transition(list_transitions):
    print("Chose transition: ")
    chose = random.choice(list_transitions)
    print (chose)
    next_state = chose[2]
    print("Now on " + str(next_state))
    return(next_state)
    
def move(initial_state, number_of_times):
    for move in range(number_of_times):
        current_state = choose_transition(list_transitions(initial_state))

move(initial_state, 10)
        


            



 
 
